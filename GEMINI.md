# Human Rater Evaluation & Rationale Guidelines (Project Cambridge / Innodata)

This rule governs all AI comparative evaluations, rationale justifications, and Google Form responses generated for Project Cambridge / Innodata / Alphabet tasks.

---

## 1. Zero AI Footprint (100% Human Score Standard)

All rationales and summaries must read as if typed by an experienced human evaluator working under a 35-minute task timer. Under no circumstances should text trigger automated AI detectors.

### Banned AI Tells & Anti-Patterns (from `Wikipedia:Signs of AI writing`, `blader`, `code20`):
* **No Negative Parallelisms (`WP:AIPARALLEL`)**: Stop contrasting everything with *"not X, but Y,"* *"Y rather than X,"* *"instead of X,"* or *"reads more like X than Y."* Just state what is on the screen directly.
* **No Copula Avoidance (`WP:AINOCOPULA`)**: Use plain *"is,"* *"are,"* and *"has."* Never dress them up with *"serves as,"* *"reads as,"* *"features,"* *"boasts,"* or *"adds a quality of."*
* **No Participle ("-ing") Tails (`WP:SUPERFICIAL`)**: Don't end sentences with dangling analysis clauses (*"..., washing out the shape,"* *"..., making it unusable"*).
* **No Rule of Three (`WP:RO3`)**: Never write neat 3-item lists or 3 parallel clauses. Stick to 1, 2, or 4+ points.
* **No Formal Transitions**: Never use `"Furthermore,"` `"Additionally,"` `"Moreover,"` `"In conclusion,"` `"It is worth noting,"` or `"In contrast."`
* **No Modern or Classic AI Vocabulary (`WP:AIVOCAB`)**: Avoid *"incorporates,"* *"contaminates,"* *"decisive gap,"* *"paramount,"* *"matters,"* *"quietly,"* *"clearer,"* *"meticulous."*
* **No AI Wrap-Up Closings (`WP:CONCLUSION`)**: Stop as soon as the point is made. No summary sentence.

### Mandatory Human Writing Characteristics (`WP:HUMANSIGNS`):
* **Heavy Use of Simple "Is" and "Has"**: Humans write *"The head has dirt on it,"* *"The frame is too close,"* *"There is green light on the rim."*
* **Plain Anglo-Saxon Vocabulary**: Use basic words: *broke, missed, forgot, looked, dirty, washed out, messed up*.
* **Direct Declarative Statements**: Say what happened without philosophical framing.
* **Natural Human Wordiness**: Use conversational phrases like *the fact that, pretty much, kind of, a whole lot of*.
* **Natural Contractions**: Always use *doesn't, isn't, there's, didn't, wasn't, can't*.

---

## 2. Technical Token Protection (`blader/humanizer`)

Always preserve the following technical artifacts verbatim:
* Exact filenames (`alien.jpg`, `alien_goggles_3d.jpg`, `Crash_Theme_Instrumental_New_Version.wav`).
* Timestamps and intervals (`0:35–0:50`, `past 1:10`).
* Rubric question tags (`Q2`, `Q5`, `Q17`).
* Technical specs (`3000x3000px`, `24-bit/48kHz WAV`).

---

## 3. SOT Compliance & Scale Calibration

1. **Mandatory 3-Part Layout**:
   ```text
   Response A defects:
   [Concrete flaws, artifacts, or missed requirements—even if A won]

   Response B defects:
   [Concrete flaws, artifacts, or missed requirements—even if B won]

   Why you chose your rating:
   [Decisive differences based on accuracy, prompt adherence, and core constraints]
   ```

2. **Flaws in Winning Response**:
   * Always document remaining minor flaws in the winning model to satisfy QA audit requirements.

3. **Scale Calibration**:
   * Compress ratings toward the center (`A is better`, `B is better`, `About the same`). Avoid `Much better` unless the losing deliverable is blank, crashed, or completely wrong.
