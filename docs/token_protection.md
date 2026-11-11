# Technical Token Protection Guide

When writing evaluations for AI data rating programs (such as Project Cambridge, Innodata, Oxford Group, or Alphabet studies), automated QA checks and time-tracking forms demand strict adherence to technical tokens.

Never allow a humanizer or rewrite pass to scramble, mutate, or paraphrase the following entities:

---

## 1. Concrete Filenames
- `alien.jpg`
- `alien_goggles_3d.jpg`
- `Crash_Theme_Instrumental_New_Version.wav`
- `Crash_Warped_Chrono_Island_Master.wav`
- `input/alien_art.png`

**Rule**: Keep extensions (`.jpg`, `.wav`, `.png`, `.mp4`) and original capitalization intact.

---

## 2. Timestamps and Durations
- `0:35–0:50`
- `past 1:10`
- `at 2:14`

**Rule**: Never convert exact timestamps into approximations like *"about a minute in"* if a specific defect happens at an exact point in time.

---

## 3. Rubric & QA Question Tags
- `Q2`, `Q5`, `Q6`, `Q17`, `Q20`, `Q22`, `Q24`, `Q31`

**Rule**: Place rubric tags in parentheses immediately following the observation they substantiate. Example:
> `That breaks the close-up requirement (Q2).`

---

## 4. Technical Specifications
- `24-bit/48kHz WAV`
- `3000 x 3000 px`
- `300 DPI`

---

## 5. SOT 3-Part Markdown Headers
The platform parser expects these three exact strings:
```text
Response A defects:

Response B defects:

Why you chose your rating:
```
Do not change them to `"Flaws in Model A:"` or `"Justification:"`.
