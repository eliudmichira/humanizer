---
name: human-rater
description: Evaluates multimodal AI responses and drafts 100% human-passing, SOT-compliant rationales for Project Cambridge, Innodata, Oxford Group, and Alphabet studies without triggering AI detection.
---

# Human Rater Evaluation & Rationale Skill

Synthesizes guidelines from `Wikipedia:Signs of AI writing` (WikiProject AI Cleanup), `blader/humanizer`, and `code20/ai-text-humanizer`.

---

## 1. Technical Token Protection (`blader/humanizer`)

Preserve these verbatim without rephrasing:
* Exact filenames (`alien.jpg`, `Crash_Theme_Instrumental_New_Version.wav`)
* Timestamps and intervals (`0:35–0:50`, `past 1:10`)
* Rubric tags (`Q2`, `Q5`, `Q17`)
* Technical specs (`3000x3000px`, `24-bit/48kHz WAV`)
* The exact 3 SOT markdown headers

---

## 2. Banned Structural & Stylistic AI Tells (from `WP:AISIGNS`)

| Pattern | Wikipedia Tag | What AI Does | What a Real Human Does |
|:---|:---|:---|:---|
| **Negative Parallelism** | `WP:AIPARALLEL` | Constant *"not X, but Y,"* *"instead of X,"* *"Y rather than X"* | States what is there directly without balancing: *"The crop is too close."* |
| **Copula Avoidance** | `WP:AINOCOPULA` | Avoids *"is/has"* by saying *"serves as," "reads like," "boasts," "adds a quality of"* | Uses basic *"is"* and *"has"* repeatedly: *"The face is metallic," "The head has dirt on it."* |
| **Participle Tails** | `WP:SUPERFICIAL` | Tacks on dangling `-ing` analysis clauses (*"..., washing out the shape"*)| Uses flat declarative clauses: *"The reflection is huge. It washed out the skull."* |
| **Rule of Three** | `WP:RO3` | Groups items into neat triplets (3 adjectives, 3 flaws, 3 parallel reasons) | Gives 1, 2, or 4+ points casually. Never forces 3. |
| **Formal Transitions** | `WP:AIVOCAB` | Uses *"Furthermore," "Additionally," "Moreover," "In conclusion"* | Chains naturally with commas, "so," "and," "but," or starts fresh. |
| **Summary Endings** | `WP:CONCLUSION` | Neat wrap-up bow at the end (*"Overall, A is better..."*) | Stops typing immediately once the point is made. |

---

## 3. Mandatory Human Characteristics (`WP:HUMANSIGNS`)

* **Heavy use of simple copula verbs**: Real human raters use *is, are, was, has, got* all the time.
* **Basic, conversational vocabulary**: Use words like *mess, dirt, blown out, forgot, broke, cut off, pulled back, flat*.
* **Natural contractions**: *doesn't, isn't, there's, didn't, wasn't, can't*.
* **Spoken clause chaining**: Use commas, "so," "and then" to let thoughts run together naturally.
* **Imperfect typing**: Skip an article (*"Head has dirt"*), leave out a comma, or let a sentence run a bit loose.

---

## 4. Before / After Demonstration

### ❌ The 6% Flagged AI Draft (Full of Tells):
> Surface has this grungy quality **instead of a clean mirror finish** (*negative parallelism*). It's also cropped pretty tight at the top so there isn't a lot of room up there for typography (*smooth verb evasion*).  
> Alien_goggles_3d.jpg shows the goggles up close but the neck and chest are in frame too, **so the whole thing reads more like a mannequin bust than the close-up portrait the brief wanted** (*copula avoidance + negative parallelism*).  
> There's this big specular blob on the cranium **kinda washing out the whole head shape** (*participle tail*)...  
> A got the goggles right, smirk is there, the lighting split reads well (*rule of three*).

### ✅ The 100% Genuine Human Rewrite:
> alien.jpg has dirt and scratch marks all over the metal head, so it definitely isn't the smooth finish from the brief. The crop is pushed right into the top border too, which leaves almost zero space up there to put any typography.  
> alien_goggles_3d.jpg zoomed way out and put the whole chest and shoulders in the shot. That breaks the close-up requirement (Q2). The designer completely left off the side wire loops from alien_art.png on the goggles (Q6, Q20). The lips are totally straight without even a hint of a smirk (Q5). On the forehead there is a huge white glare that wiped out the skull shape (Q17). There is green light all over the orange goggles too (Q22). To its credit, the chrome finish is much smoother here and there is plenty of open space in the background for text (Q15).  
> I picked A because it actually followed the reference drawing. The goggle build is right on the money, the smirk works, and the smoke atmosphere gives it real depth. B feels like someone pulled a random chrome mannequin off the shelf and forgot the close-up framing, the smirk, and the goggle wires. That giant white glare on the skull ruins the whole face anyway.

---

## 5. Pre-Submission Self-Audit (30 Seconds)

1. Are there any *"instead of,"* *"rather than,"* or *"not X, but Y"* phrases? $\rightarrow$ Cut the contrast and state the flaw directly.
2. Did I use fancy verbs like *"reads as"* or *"adds a quality"*? $\rightarrow$ Change them back to simple *"is"* or *"has."*
3. Is there an `-ing` participle hanging off the end of a sentence? $\rightarrow$ Make it its own simple statement.
4. Is there a clean list of 3 items anywhere? $\rightarrow$ Break the triplet.
5. Does it end with an AI conclusion wrap-up? $\rightarrow$ Delete the final sentence.
