#!/usr/bin/env python3
"""
Humanizer Audit CLI
Scans text or markdown files for AI writing tells based on Wikipedia:Signs_of_AI_writing,
blader/humanizer, and code20 guidelines.
"""

import sys
import re
import argparse
import statistics

# Banned transitional starters
FORMAL_TRANSITIONS = [
    r"\bfurthermore\b", r"\badditionally\b", r"\bmoreover\b",
    r"\bin conclusion\b", r"\bit is worth noting\b", r"\bin contrast\b",
    r"\bconsequently\b", r"\bnotably\b"
]

# AI Vocabulary & inflated buzzwords
AI_VOCABULARY = [
    r"\bincorporates?\b", r"\bcontaminates?\b", r"\bdecisive gap\b",
    r"\bparamount\b", r"\bmeticulous(?:ly)?\b", r"\bexemplary\b",
    r"\bsubstantially superior\b", r"\bcritical discrepancy\b",
    r"\bsignificantly more faithful\b", r"\bdelve\b", r"\btapestry\b",
    r"\btestament\b", r"\bunderscores?\b", r"\bexhibits?\b"
]

# Negative parallelisms (WP:AIPARALLEL)
NEGATIVE_PARALLELISMS = [
    r"\binstead of\b", r"\brather than\b", r"\bnot only\b.*?\bbut also\b",
    r"\breads more like\b.*?\bthan\b", r"\bnot just\b.*?\bbut\b"
]

# Copula avoidance (WP:AINOCOPULA)
COPULA_AVOIDANCE = [
    r"\bserves as\b", r"\breads as\b", r"\badds a quality of\b",
    r"\bboasts a\b", r"\bfeatures a\b", r"\boperates as\b"
]

# Participle tails at clause/sentence ends (WP:SUPERFICIAL)
PARTICIPLE_TAILS = [
    r",\s+(?:washing|making|ensuring|highlighting|contributing|reflecting|symbolizing|enhancing)\b"
]

def analyze_text(text: str):
    print("=" * 60)
    print("HUMANIZER HEURISTIC AUDIT REPORT")
    print("=" * 60)

    # 1. Split into sentences
    raw_sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s.strip() for s in raw_sentences if s.strip() and not s.strip().endswith(":")]

    total_words = len(text.split())
    print(f"Total Word Count: {total_words}")
    print(f"Total Sentences: {len(sentences)}")

    # 2. Burstiness & Sentence Length Variance
    lengths = [len(s.split()) for s in sentences]
    if lengths:
        mean_len = statistics.mean(lengths)
        stdev_len = statistics.stdev(lengths) if len(lengths) > 1 else 0
        print(f"Average Sentence Length: {mean_len:.1f} words")
        print(f"Sentence Length Variation (StDev): {stdev_len:.1f}")
        if stdev_len < 3.5:
            print("  ⚠️ WARNING: Low burstiness detected (uniform sentence lengths trigger AI scanners).")
        else:
            print("  ✅ Good sentence length variety (burstiness).")

    # 3. Pattern Matching
    issues = []
    
    for i, s in enumerate(sentences, 1):
        s_lower = s.lower()
        
        # Transitions
        for pat in FORMAL_TRANSITIONS:
            if re.search(pat, s_lower):
                issues.append((i, "Formal Transition", re.search(pat, s_lower).group(), s))
                
        # AI Vocabulary
        for pat in AI_VOCABULARY:
            if re.search(pat, s_lower):
                issues.append((i, "AI Vocabulary", re.search(pat, s_lower).group(), s))
                
        # Negative Parallelisms
        for pat in NEGATIVE_PARALLELISMS:
            if re.search(pat, s_lower):
                issues.append((i, "Negative Parallelism (WP:AIPARALLEL)", re.search(pat, s_lower).group(), s))
                
        # Copula Avoidance
        for pat in COPULA_AVOIDANCE:
            if re.search(pat, s_lower):
                issues.append((i, "Copula Avoidance (WP:AINOCOPULA)", re.search(pat, s_lower).group(), s))

        # Participle Tails
        for pat in PARTICIPLE_TAILS:
            if re.search(pat, s_lower):
                issues.append((i, "Participle Tail (WP:SUPERFICIAL)", re.search(pat, s_lower).group(), s))

    print("\n" + "-" * 60)
    print("DETECTION FINDINGS:")
    print("-" * 60)
    
    if not issues:
        print("✅ Zero critical AI writing patterns detected! Clean human profile.")
    else:
        print(f"⚠️ Found {len(issues)} pattern violations:")
        for idx, issue_type, match_str, sentence in issues:
            print(f"  • Sentence {idx} [{issue_type}]: Matched '{match_str}'")
            print(f"    Excerpt: \"{sentence[:100]}...\"")

    # 4. Copula Ratio Check
    copula_count = len(re.findall(r"\b(is|are|was|were|has|have|had)\b", text, re.IGNORECASE))
    copula_ratio = (copula_count / total_words) * 100 if total_words > 0 else 0
    print("\n" + "-" * 60)
    print("COPULA DENSITY (WP:HUMANSIGNS):")
    print("-" * 60)
    print(f"Copula words ('is/are/was/has'): {copula_count} ({copula_ratio:.1f}% of text)")
    if copula_ratio < 2.0:
        print("  ⚠️ Low copula density. Human raters heavily favor simple 'is' and 'has'.")
    else:
        print("  ✅ Healthy natural copula usage.")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Audit text for AI writing patterns.")
    parser.add_argument("--text", type=str, help="Text string to evaluate")
    parser.add_argument("--file", type=str, help="Path to text or markdown file")
    args = parser.parse_args()

    content = ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    elif args.text:
        content = args.text
    else:
        # Read from stdin
        content = sys.stdin.read()

    if not content.strip():
        print("No content provided to audit.")
        sys.exit(1)

    analyze_text(content)

if __name__ == "__main__":
    main()
