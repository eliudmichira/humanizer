#!/usr/bin/env python3
"""
Humanizer audit: a style linter for the patterns catalogued in
Wikipedia:Signs of AI writing (see docs/wikipedia_tells.md).

It reports where a draft uses those patterns and how densely, so an editor
knows where to look. It is not an AI detector. It cannot tell who or what
wrote a text, every pattern here also occurs in human writing, and a low
score does not mean a text will be judged human by any tool or reader.

Usage:
    python humanizer_audit.py --file draft.md
    python humanizer_audit.py --text "Some text to check."
    cat draft.md | python humanizer_audit.py --json
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import asdict, dataclass

FLAGS = re.IGNORECASE | re.MULTILINE


@dataclass(frozen=True)
class Category:
    key: str
    label: str
    ref: str
    weight: float
    fix: str
    patterns: tuple[str, ...]
    raw: bool = False  # scan the unmasked text (URLs and code included)


@dataclass
class Finding:
    category: str
    line: int
    match: str
    excerpt: str
    weight: float


CATEGORIES: tuple[Category, ...] = (
    # ---- Tier 1: remove on sight -------------------------------------
    Category(
        "residue", "Chatbot conversation left in the text", "WP:CERTAINLY", 5,
        "Delete it.",
        (
            r"\bas an? (?:ai|large) language model\b",
            r"\bi hope this helps\b",
            r"(?:^|[\s\"“])(?:certainly|of course|absolutely)!",
            r"\byou(?:'|’)re absolutely right\b",
            r"\bwould you like (?:me to|help|a)\b",
            r"\blet me know if\b",
            r"\bis there anything else\b",
            r"\bhere(?:'s|’s| is) (?:a|an|the|your) (?:[\w-]+ ){0,3}"
            r"(?:version|draft|rewrite|summary|breakdown|overview|article|outline)\b",
            r"\bmore detailed breakdown\b",
            r"\b(?:as of|up to) my last (?:knowledge|training) (?:update|cutoff)\b",
            r"\bi (?:cannot|can't|can’t) (?:offer|provide|directly)\b",
        ),
    ),
    Category(
        "placeholder", "Unfilled placeholder", "WP:AIPLACEHOLDER", 5,
        "Fill in the real value or remove the sentence. Do not guess.",
        (
            r"\[(?:your|insert|add|name|year|date|founder|company|entertainer|url|link|"
            r"citation|source|title)\b[^\]\n]*\]",
            r"\((?:add|insert) (?:your|a|the)\b[^)\n]*\)",
            r"\b(?:19|20)\d\d-xx-xx\b",
            r"\bINSERT_[A-Z_]+",
            r"\bexample\.com/[\w./-]+",
            r"\bto be supplied\b",
        ),
        raw=True,
    ),
    Category(
        "artifact", "Leaked chatbot machinery", "WP:AIMARKDOWN", 5,
        "Strip the artifact, then check the link supports the sentence.",
        (
            r"contentReference",
            r"\boaicite\b",
            r"utm_source=(?:chatgpt\.com|openai|copilot\.com)",
            r"referrer=grok\.com",
            r"↩",
        ),
        raw=True,
    ),
    # ---- Tier 2: content that says nothing ---------------------------
    Category(
        "significance", "Inflated significance", "WP:AILEGACY", 3,
        "State the fact that would justify the claim, or cut the claim.",
        (
            r"\b(?:is|are|was|were|stands? as|serves? as) (?:a|an) (?:\w+ )?(?:testament|reminder)\b",
            r"\ba testament to\b",
            r"\b(?:plays?|played|playing) (?:a|an) (?:\w+ )?"
            r"(?:crucial|pivotal|vital|significant|key|central|important) role\b",
            r"\b(?:crucial|pivotal|key|defining|watershed) (?:moment|turning point)\b",
            r"\b(?:underscor|highlight)(?:es|ed|ing) (?:its|the|their|his|her) "
            r"(?:importance|significance|relevance)\b",
            r"\breflects? (?:a )?broader\b",
            r"\bsetting the stage for\b",
            r"\b(?:ever-)?evolving landscape\b",
            r"\bindelible mark\b",
            r"\bdeeply rooted\b",
            r"\bfocal point\b",
            r"\b(?:enduring|lasting) (?:legacy|impact|influence)\b",
            r"\b(?:marks?|marked|represents?|represented) a (?:\w+ )?shift\b",
        ),
    ),
    Category(
        "attribution", "Vague attribution or source-describing", "WP:AIWEASEL", 3,
        "Name who said it and what they said, or cut it.",
        (
            r"\b(?:experts?|scholars|critics|observers|analysts|researchers) "
            r"(?:have )?(?:argue|say|believe|agree|note|suggest|point out|cited|noted|argued)\b",
            r"\bsome critics\b",
            r"\bindustry (?:reports?|observers|experts|analysts)\b",
            r"\bwidely (?:regarded|recognized|recognised|considered|acknowledged|associated)\b",
            r"\bseveral (?:sources|publications|outlets)\b",
            r"\bindependent coverage\b",
            r"\b(?:local|regional|national|trade|business|tech|music) (?:media )?(?:outlets|publications)\b",
            r"\b(?:active|strong|robust) (?:social media|digital|online) presence\b",
        ),
    ),
    Category(
        "identification", "Vague connection or identification by sources", "WP:AICONNECT", 2,
        "State the relationship or fact directly: 'was CEO of', 'taught at'.",
        (
            r"\bidentif(?:y|ies|ied) (?:him|her|them|it|the \w+) as\b",
            r"\b(?:was|were|is|are) identified (?:by [^.\n]{1,40} )?as\b",
            r"\b(?:profile|website|records?|listings?|filings?|databases?) "
            r"(?:lists?|identif(?:y|ies)|describes?)\b",
            r"\b(?:associated|connected) (?:with|to)\b",
            r"\bin (?:connection|association) with\b",
        ),
    ),
    Category(
        "disclaimer", "Disclaimer about information or sources", "WP:AIDISCLAIMER", 3,
        "Delete. If there is a real limitation, state it once as a fact.",
        (
            r"\bwhile (?:specific |exact |precise )?(?:details|information|data) "
            r"(?:are|is|remains?) (?:limited|scarce|sparse)\b",
            r"\bnot (?:widely|publicly) (?:available|documented|disclosed|known)\b",
            r"\bbased on (?:the )?available information\b",
            r"\bin the (?:provided|available) (?:sources|search results)\b",
            r"\bdoes not by itself establish\b",
            r"\bshould (?:be|not be) (?:treated|presented|understood|read|interpreted) as\b",
            r"\bshould not be confused with\b",
            r"\bit(?:'s|’s| is) (?:important|worth|crucial|essential) "
            r"(?:to (?:note|remember|recognize)|noting)\b",
            r"\bmaintains? a low profile\b",
        ),
    ),
    Category(
        "challenges", "Challenges and future-prospects formula", "WP:FACESCHALLENGES", 3,
        "Report the specific problem where it belongs and drop the reassurance.",
        (
            r"\bdespite (?:its|their|his|her|these|this|the)\b[^.\n]{0,80}?"
            r"\b(?:faces?|faced|challenges?)\b",
            r"\bfaces? (?:several|numerous|many|significant|a number of) challenges\b",
            r"\bfuture (?:outlook|prospects)\b",
        ),
    ),
    Category(
        "ing_tail", "Trailing '-ing' analysis", "WP:SUPERFICIAL", 2,
        "Cut the clause, or give the claim its own sentence with a subject.",
        (
            r",\s+(?:highlighting|underscoring|emphasizing|emphasising|ensuring|reflecting|"
            r"symbolizing|symbolising|contributing to|cultivating|fostering|encompassing|"
            r"enhancing|showcasing|demonstrating|solidifying|cementing|making it|"
            r"allowing (?:it|them|users)|paving the way)\b",
            r"\bvaluable insights?\b",
            r"\b(?:align|resonate)(?:s|d|ed)? with\b",
        ),
    ),
    Category(
        "conclusion", "Summary ending", "WP:CONCLUSION", 2,
        "Delete. End on the last piece of content.",
        (
            r"(?:^|(?<=[.!?]\s))(?:in (?:conclusion|summary)|overall|to sum up|ultimately|"
            r"in essence),",
        ),
    ),
    # ---- Tier 3: sentence habits -------------------------------------
    Category(
        "copula", "Copula avoidance", "WP:AINOCOPULA", 2,
        "Write 'is', 'are', 'has'.",
        (
            r"\b(?:serves?|served|serving|stands?|stood|functions?|functioned|"
            r"operates?|operated) as (?:a|an|the)\b",
            r"\bholds? the distinction of\b",
            r"\bboasts? (?:a|an|the|over|more|some|\d)",
            r"\bfeatures (?:a|an)\b",
            r"\bventured into\b",
        ),
    ),
    Category(
        "parallelism", "Negative parallelism", "WP:AIPARALLEL", 2,
        "State the point. Keep the contrast only if readers would assume the opposite.",
        (
            r"\bnot only\b[^.\n]{1,120}?\bbut\b",
            r"\bnot (?:just|merely|simply)\b[^.\n]{1,120}?(?:\bbut\b|[;,—–-]\s*it(?:'s|’s| is)\b)",
            r"\bit(?:'s|’s| is)(?: not|n't|n’t)\b[^.\n]{1,80}?[,;—–]\s*it(?:'s|’s| is)\b",
            r"\bno [\w-]+, no [\w-]+[,.]? just\b",
            r"\brather than\b",
            r"\binstead of\b",
        ),
    ),
    Category(
        "vocabulary", "AI vocabulary", "WP:AIVOCAB", 1,
        "Use the plain word. Only a cluster matters; one hit is nothing.",
        (
            r"\badditionally\b", r"\balign(?:s|ed|ing)? with\b", r"\bbolster(?:s|ed|ing)?\b",
            r"\bcrucial\b", r"\bdeep dive\b", r"\bdelv(?:e|es|ed|ing)\b",
            r"\bemphasi[sz]ing\b", r"\benduring\b", r"\benhanc(?:e|es|ed|ing)\b",
            r"\bfoster(?:s|ed|ing)?\b", r"\bgarner(?:s|ed|ing)?\b",
            r"\bhighlight(?:s|ed|ing)\b", r"\binterplay\b", r"\bintrica(?:te|cies)\b",
            r"\b(?:[\w-]+ landscape of|(?:digital|media|political|cultural|business|"
            r"competitive|technological|regulatory|changing) landscape)\b",
            r"\bmeticulous(?:ly)?\b", r"\bpivotal\b", r"\brobust\b",
            r"\bshowcas(?:e|es|ed|ing)\b", r"\btapestry\b", r"\btestament\b",
            r"\bunderscor(?:e|es|ed|ing)\b", r"\bvaluable\b", r"\bvibrant\b",
            # mid-2026 set (ordinary words such as 'matters' and 'practical' are left out)
            r"\bleverag(?:e|es|ed|ing)\b", r"\bmultifaceted\b", r"\bprioriti[sz](?:e|es|ed|ing)\b",
            r"\bquietly\b", r"\bdependable\b", r"\buniversally\b",
        ),
    ),
    Category(
        "transition", "Formal transition opening a sentence", "WP:AIVOCAB", 1,
        "Weak on its own. Drop it or join the sentences.",
        (
            r"(?:^|(?<=[.!?]\s))(?:furthermore|moreover|additionally|consequently|notably|"
            r"importantly|in addition),",
        ),
    ),
    Category(
        "stiff", "Stiff synonym", "WP:HUMANSIGNS", 1,
        "Use the ordinary word: used, wrote, moved, tried, started, died.",
        (
            r"\butili[sz](?:e|es|ed|ing)\b", r"\bauthored\b", r"\brelocated\b",
            r"\bcommenc(?:e|es|ed|ing)\b", r"\bpassed away\b", r"\bendeavou?r(?:s|ed|ing)?\b",
        ),
    ),
    Category(
        "puffery", "Promotional language", "WP:AIPUFFERY", 2,
        "Replace the adjective with the fact behind it, or cut it.",
        (
            r"\bnestled\b", r"\bin the heart of\b", r"\bgroundbreaking\b", r"\brenowned\b",
            r"\bdiverse array\b", r"\bnatural beauty\b", r"\brich (?:cultural )?heritage\b",
            r"\bcommitment to (?:excellence|quality|innovation|sustainability)\b",
            r"\bbreathtaking\b", r"\bworld-class\b", r"\bseamless(?:ly)?\b",
        ),
    ),
)

STYLE_LABELS = {
    "style": ("Formatting", "WP:AISIGNS/Style", "Match the destination's conventions."),
    "rhythm": ("Uniform rhythm and punctuation", "WP:AIDASH",
               "Let sentence length follow content; use the mark each sentence needs."),
    "triplet": ("Possible rule of three", "WP:RO3",
                "Count the real items. Drop a third that was added for rhythm."),
}

FENCE = re.compile(r"^(```|~~~)[^\n]*\n.*?^\1[^\n]*$", re.DOTALL | re.MULTILINE)
INLINE_CODE = re.compile(r"`[^`\n]+`")
URL = re.compile(r"https?://[^\s)>\]]+")
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’-]*")
EMOJI = "\U0001F300-\U0001FAFF☀-➿⭐⭕"
SMALL_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "nor", "of", "on",
               "or", "the", "to", "vs", "via", "with"}


def _blank(match: re.Match) -> str:
    """Replace a span with spaces, keeping newlines so line numbers survive."""
    return re.sub(r"[^\n]", " ", match.group())


def mask(text: str) -> str:
    """Blank out code and URLs so technical tokens are never flagged as prose."""
    for rx in (FENCE, INLINE_CODE, URL):
        text = rx.sub(_blank, text)
    return text


def _line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _excerpt(text: str, pos: int, limit: int = 110) -> str:
    start = text.rfind("\n", 0, pos) + 1
    end = text.find("\n", pos)
    line = text[start:end if end != -1 else len(text)].strip()
    if len(line) <= limit:
        return line
    lo = max(0, pos - start - limit // 2)
    return ("…" if lo else "") + line[lo:lo + limit].strip() + "…"


def prose_only(masked: str) -> str:
    """Drop headings, table rows and list markers; keep sentence text."""
    out = []
    for line in masked.splitlines():
        s = line.strip()
        if s.startswith("#") or s.startswith("|"):
            continue
        s = re.sub(r"^(?:[-*+•>]|\d+[.)])\s+", "", s)
        out.append(s)
    return "\n".join(out)


def sentences(prose: str) -> list[str]:
    flat = re.sub(r"\s*\n\s*", " ", re.sub(r"\n\s*\n", ". ", prose))
    parts = re.split(r"(?<=[.!?])[\"”’)]*\s+", flat)
    return [p for p in parts if len(WORD.findall(p)) >= 2]


def pattern_findings(raw: str, masked: str) -> list[Finding]:
    found: list[Finding] = []
    for cat in CATEGORIES:
        text = raw if cat.raw else masked
        seen: set[tuple[int, int]] = set()
        for pat in cat.patterns:
            for m in re.finditer(pat, text, FLAGS):
                if m.span() in seen or not m.group().strip():
                    continue
                seen.add(m.span())
                found.append(Finding(cat.key, _line_of(text, m.start()),
                                     " ".join(m.group().split()),
                                     _excerpt(raw, m.start()), cat.weight))
    return found


def style_findings(raw: str, masked: str, n_words: int) -> list[Finding]:
    found: list[Finding] = []

    def add(cat: str, pos: int, match: str, weight: float, excerpt: str | None = None):
        found.append(Finding(cat, _line_of(masked, pos), match,
                             excerpt if excerpt is not None else _excerpt(raw, pos), weight))

    # Emoji leading a heading or list item
    for m in re.finditer(rf"^[ \t]*(?:#{{1,6}}[ \t]+|[-*+•][ \t]+)?[{EMOJI}]", masked, re.M):
        add("style", m.start(), "emoji at start of heading or list item", 2)

    # Inline-header list items: "- **Label**: text" or "**Label:** text"
    for m in re.finditer(r"^[ \t]*(?:[-*+•]|\d+[.)])[ \t]+\*\*[^*\n]+?(?::\*\*|\*\*[ \t]*[:–—-])",
                         masked, re.M):
        add("style", m.start(), "inline-header list item", 1)

    # Title Case Headings (weak: many style guides require them)
    for m in re.finditer(r"^#{1,6}[ \t]+(.+)$", masked, re.M):
        words = [w for w in re.findall(r"[A-Za-z][A-Za-z'’-]*", m.group(1))]
        rest = [w for w in words[1:] if w.lower() not in SMALL_WORDS]
        if len(rest) >= 2 and all(w[0].isupper() for w in rest):
            add("style", m.start(), "title-case heading", 0.5)

    # Boldface density in running prose
    body = "\n".join(l for l in masked.splitlines() if not l.lstrip().startswith(("#", "|")))
    bolds = re.findall(r"\*\*[^*\n]+\*\*", body)
    if len(bolds) >= 4 and n_words and len(bolds) / n_words > 1 / 60:
        add("style", masked.find("**"), f"{len(bolds)} bold spans in {n_words} words", 2,
            "boldface is scattered through the prose")

    # Curly quotes (weak: word processors add them)
    curly = len(re.findall(r"[“”‘’]", masked))
    if curly >= 4:
        add("style", re.search(r"[“”‘’]", masked).start(), f"{curly} curly quotes/apostrophes", 0.5,
            "curly quotation marks; check the destination's convention")

    # Em dashes
    dashes = [m.start() for m in re.finditer("—", masked)]
    if len(dashes) >= 3 and n_words and len(dashes) / n_words > 5 / 1000:
        spaced = len(re.findall(r"\s—\s", masked))
        add("rhythm", dashes[0], f"{len(dashes)} em dashes ({spaced} spaced)", 2,
            "em dashes are doing the work of commas, colons and parentheses")

    prose = prose_only(masked)

    # The opposite problem: nothing but commas and periods
    if n_words >= 200 and not re.search(r"[;:()—–]", prose):
        add("rhythm", 0, "only commas and periods", 2,
            f"no colons, semicolons, parentheses or dashes in {n_words} words")

    # Sentence-length uniformity
    lengths = [len(WORD.findall(s)) for s in sentences(prose)]
    if len(lengths) >= 10:
        band = sum(1 for n in lengths if 8 <= n <= 20) / len(lengths)
        if band >= 0.9:
            add("rhythm", 0, f"{band:.0%} of sentences are 8-20 words", 2,
                "sentence lengths sit in a narrow band")
    if len(lengths) >= 6 and statistics.stdev(lengths) < 3.5:
        add("rhythm", 0, f"sentence-length stdev {statistics.stdev(lengths):.1f}", 1,
            "sentences are nearly all the same length")

    # Rule of three: "a, b, and c" where the list is exactly three items long
    item = r"[A-Za-z][\w'’-]*(?: [\w'’-]+){0,2}"
    for m in re.finditer(rf"\b{item}, {item},? and {item}", masked):
        before = masked[:m.start()].rstrip()
        after = masked[m.end():m.end() + 6]
        if before.endswith(",") or re.match(r",? (?:and|or)\b", after):
            continue  # part of a longer list
        add("triplet", m.start(), " ".join(m.group().split()), 1)

    return found


def audit(text: str) -> dict:
    masked = mask(text)
    n_words = len(WORD.findall(prose_only(masked)))
    findings = pattern_findings(text, masked) + style_findings(text, masked, n_words)
    findings.sort(key=lambda f: (f.line, f.category))

    lengths = [len(WORD.findall(s)) for s in sentences(prose_only(masked))]
    total = sum(f.weight for f in findings)
    score = round(total / n_words * 100, 2) if n_words else 0.0
    band = "low" if score < 1 else "moderate" if score <= 3 else "high"
    families = len({f.category for f in findings})

    return {
        "words": n_words,
        "sentences": len(lengths),
        "mean_sentence_length": round(statistics.mean(lengths), 1) if lengths else 0,
        "sentence_length_stdev": round(statistics.stdev(lengths), 1) if len(lengths) > 1 else 0,
        "findings": [asdict(f) for f in findings],
        "pattern_families": families,
        "weighted_hits": total,
        "density": score,
        "band": band,
    }


def _meta(key: str) -> tuple[str, str, str]:
    for cat in CATEGORIES:
        if cat.key == key:
            return cat.label, cat.ref, cat.fix
    return STYLE_LABELS[key]


def render(report: dict) -> str:
    out = ["=" * 68, "HUMANIZER AUDIT  (style linter, not an AI detector)", "=" * 68]
    out.append(f"Words: {report['words']}   Sentences: {report['sentences']}   "
               f"Mean length: {report['mean_sentence_length']}   "
               f"Stdev: {report['sentence_length_stdev']}")
    out.append(f"Pattern density: {report['density']} weighted hits per 100 words "
               f"({report['band']}), across {report['pattern_families']} pattern families")

    findings = report["findings"]
    if not findings:
        out += ["", "No catalogued patterns found. Leave the text alone.", "=" * 68]
        return "\n".join(out)

    groups: dict[str, list[dict]] = {}
    for f in findings:
        groups.setdefault(f["category"], []).append(f)
    ordered = sorted(groups.items(), key=lambda kv: -sum(f["weight"] for f in kv[1]))

    for key, items in ordered:
        label, ref, fix = _meta(key)
        out += ["", f"{label}  [{ref}]  x{len(items)}", f"  Fix: {fix}"]
        for f in items[:8]:
            out.append(f"  L{f['line']:<4} '{f['match']}'")
            if f["excerpt"] and f["excerpt"] != f["match"]:
                out.append(f"        {f['excerpt']}")
        if len(items) > 8:
            out.append(f"  ... and {len(items) - 8} more")

    out += ["", "-" * 68]
    if report["band"] == "low":
        out.append("Few hits. Fix any tier-1 items above and otherwise edit lightly.")
    elif report["band"] == "moderate":
        out.append("Some clustering. Start with the groups at the top of this list.")
    else:
        out.append("Dense clustering. The draft needs a full pass, starting with content.")
    out.append("Every pattern here also occurs in human writing. Judge clusters, not single hits.")
    out.append("=" * 68)
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lint text for the patterns in Wikipedia:Signs of AI writing.")
    parser.add_argument("--text", help="text to check")
    parser.add_argument("--file", help="path to a text or Markdown file")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument("--fail-over", type=float, metavar="DENSITY",
                        help="exit with status 1 if density exceeds this value")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            content = fh.read()
    elif args.text is not None:
        content = args.text
    else:
        content = sys.stdin.read()

    if not content.strip():
        print("No content provided to audit.", file=sys.stderr)
        return 2

    report = audit(content)
    print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else render(report))
    if args.fail_over is not None and report["density"] > args.fail_over:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
