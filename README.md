# Humanizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An agent skill and a small linter for editing prose that reads like chatbot output. The skill rewrites a draft into plain, specific language in the author's voice. The linter shows where a draft uses the patterns catalogued in Wikipedia's "Signs of AI writing" and how densely.

Sources:

- [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup): the pattern catalog, as of 10 November 2026
- [blader/humanizer](https://github.com/blader/humanizer): protecting code, commands, paths, URLs, and other technical tokens
- [code20/ai-text-humanizer](https://github.com/code20/ai-text-humanizer): preserve facts, restructure for flow, never invent detail

## What it does and does not do

It edits for readers. The Wikipedia page makes the point that each sign is a symptom: a sentence about a subject's "pivotal role in the evolving landscape" is a problem because it says nothing a reader can check, and swapping in a synonym leaves that problem in place. So the skill cuts or sharpens the content first and treats wording second.

It does not promise anything about AI detectors. Detection tools have real error rates and react to trivial changes, so no rule set can guarantee a score, and a score is a poor measure of writing. The skill also will not fake human authorship (deliberate typos, invented experience) or help present AI-written work as human-written where a platform, client, or institution requires human work.

## The approach

| Tier | What | Examples | Action |
|---|---|---|---|
| 1 | Chatbot leftovers | "Certainly!", `[Your Name]`, `utm_source=chatgpt.com`, `2025-XX-XX` | Remove on sight; flag placeholders |
| 2 | Content that says nothing | inflated significance, "experts argue", trailing "-ing" analysis, source disclaimers, "Despite these challenges…" | State the fact or cut the sentence |
| 3 | Sentence habits | "serves as", "not just X but Y", "rather than", forced triplets, AI vocabulary, uniform 8 to 20 word sentences | Fix clusters; leave single instances |
| 4 | Formatting | scattered bold, `**Label**:` bullets, emoji headings, em dash overuse | Match the destination |

Rules that hold throughout: keep every fact, add none, copy technical tokens exactly, and never repair a citation from memory. `SKILL.md` also has a "Do not overcorrect" section, because a rewrite that bans words mechanically or chops everything into short sentences is as recognizable as the original.

## Repository layout

```text
humanizer/
├── SKILL.md                  # the skill: rules, process, modes, output format
├── humanizer_audit.py        # linter for the catalogued patterns
├── docs/
│   ├── wikipedia_tells.md    # full catalog: word lists, eras, strength, fixes
│   └── token_protection.md   # rater-task token list
├── tests/
│   └── test_audit.py
├── GEMINI.md                 # rater-task workspace rules
└── examples/
    └── alien_art_case.md     # rater-task case study
```

`GEMINI.md`, `docs/token_protection.md`, and `examples/alien_art_case.md` predate the general skill and are specific to one evaluation-rationale workflow. The general skill does not depend on them.

## Linter

```bash
python humanizer_audit.py --file draft.md
```

```bash
python humanizer_audit.py --text "The museum stands as a testament to the city's vibrant history."
```

```bash
cat draft.md | python humanizer_audit.py --json
```

Use `--fail-over 3` to exit with status 1 when density is above 3 weighted hits per 100 words, for use in CI.

The report groups hits by pattern family, most serious first, with line numbers and the suggested fix. Fenced code, inline code, and URLs are skipped, so quote sample text as a blockquote if you want it checked. Requires Python 3.9 or later and no packages.

Run the tests with:

```bash
python -m unittest discover -s tests
```

The linter is a set of regular expressions. It finds wording, it cannot judge whether a contrast is real or a list truly has three items, and it says nothing about who wrote a text. Every pattern it flags also occurs in human writing.

## Installing the skill

Claude Code: copy `SKILL.md` to `~/.claude/skills/humanizer/SKILL.md` (or `.claude/skills/humanizer/SKILL.md` in a project), with `docs/wikipedia_tells.md` and `humanizer_audit.py` alongside it.

Antigravity: copy the same files to `.agents/skills/humanizer/` in a project, or `~/.gemini/config/skills/humanizer/` globally.

Cursor and other agents: paste the "Hard rules", "The patterns", and "Do not overcorrect" sections of `SKILL.md` into the rules file.

## Licensing note

`docs/wikipedia_tells.md` is adapted from Wikipedia text and is shared under CC BY-SA 4.0, as that license requires.
