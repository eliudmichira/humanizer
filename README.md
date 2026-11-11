# Humanizer: AI Detector Evasion & Human Rationale Framework

[![Skill Compatible](https://img.shields.io/badge/Antigravity-Skill-blue.svg)](https://github.com/eliudmichira/humanizer)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An agent skill, heuristic rule engine, and evaluation rationale framework built to eliminate AI writing signatures and pass automated AI detectors with **100% Human** scores under tight deadlines.

Synthesizes empirical findings and rules from:
- [**`Wikipedia:Signs of AI writing`** (WikiProject AI Cleanup)](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [**`blader/humanizer`** (Technical Token Protection)](https://github.com/blader/humanizer)
- [**`code20/ai-text-humanizer`** (Anti-Slop Rewriting & Flow)](https://github.com/code20/ai-text-humanizer)
- [**`AIHumanizerBenchmark`** (Factual Integrity)](https://github.com/AIHumanizerBenchmark/AIHumanizerBenchmark)

---

## The Core Philosophy: Restructure, Don't Synonym-Spin

Commercial "humanizer" tools rely on aggressive thesaurus spinning, generating bizarre, unreadable phrases like:
> ❌ *"retro-industrial fact-winged curves side girational wires"*

Real human raters typing under a 35-minute timer don't use spinners; they use **blunt observations, simple copulas (*is, has*), and colloquial connectors**:
> ✅ *"alien_goggles_3d.jpg zoomed way out and put the whole chest in the shot. That breaks the close-up requirement (Q2)."*

This repository provides both the rules (`SKILL.md`, `GEMINI.md`) and a Python auditing CLI (`humanizer_audit.py`) to detect and strip AI tells before submission.

---

## The 5 Core AI Tells We Eliminate

| Pattern | Wikipedia Citation | What AI Models Do | What Real Humans Do |
|:---|:---|:---|:---|
| **Negative Parallelisms** | `WP:AIPARALLEL` | Overuses *"not X, but Y,"* *"instead of X,"* *"Y rather than X"* | States the flaw directly: *"The metal has dirt on it."* |
| **Copula Avoidance** | `WP:AINOCOPULA` | Swaps simple *"is/has"* for *"reads as,"* *"serves as,"* *"boasts"* | Uses basic copula verbs (*is, are, was, has, got*) repeatedly. |
| **Participle Tails** | `WP:SUPERFICIAL` | Tacks dangling `-ing` clauses at sentence ends (*"..., washing out the shape"*) | Uses separate flat clauses: *"The glare is huge. It washed out the skull."* |
| **Rule of Three** | `WP:RO3` | Constantly formats lists and reasons into clean triplets | Lists 1, 2, or 4+ points casually. Never forces 3. |
| **Wrap-Up Closings** | `WP:CONCLUSION` | Closes with neat summary sentences (*"Overall, A is better..."*) | Stops immediately once the decisive difference is stated. |

---

## Repository Structure

```text
humanizer/
├── SKILL.md                # Agent skill for Antigravity, Claude Code, and cursor agents
├── GEMINI.md               # Contextual workspace rule file for LLM pair-programmers
├── humanizer_audit.py      # Python script that scores text burstiness and flags AI patterns
├── docs/
│   ├── wikipedia_tells.md  # Deep dive into WP:AISIGNS and empirical linguistic shifts
│   └── token_protection.md# Best practices for preserving technical tokens verbatim
└── examples/
    ├── alien_art_case.md   # Side-by-side progression (0% -> 6% -> 100% Human)
    └── audio_remake_case.md# Multimodal music recreation task evaluation
```

---

## Python Audit Tool Usage

Run the built-in heuristic scanner to test any rationale draft before pasting:

```bash
python humanizer_audit.py --text "In alien.jpg, the head has dirt marks instead of smooth chrome."
```

Or scan a file:
```bash
python humanizer_audit.py --file examples/alien_art_case.md
```

---

## Installation in Coding Assistants

### For Antigravity
1. Copy `SKILL.md` into your project's `.agents/skills/human-rater/SKILL.md` (or globally in `~/.gemini/config/skills/human-rater/SKILL.md`).
2. Include `GEMINI.md` in your project root.

### For Claude Code / Cursor
Add the rules from `GEMINI.md` to your `.cursorrules` or `CLAUDE.md`.
