# AI writing tells: reference catalog

Adapted from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup), as it stood on 10 November 2026. The Wikipedia text is licensed CC BY-SA 4.0, and this adaptation is shared under the same license. Shortcuts such as `WP:AIPARALLEL` point back to the section each entry comes from.

`SKILL.md` holds the working rules. This file is the lookup table behind them: every pattern, the words that mark it, when it was common, how much weight it deserves, and what to do about it.

## How to read this catalog

Four points from the source page govern everything below.

1. **The list is descriptive.** It records what chatbots tend to do. It is a set of observations and was never meant as a list of banned words. Models are trained on human writing, so every pattern here also appears in human text.
2. **Density is the signal.** One "crucial" or one "rather than" means nothing. Several patterns from different families in one short passage means a lot. The vocabulary words "often co-occur: where there is one, there are likely others."
3. **The sign is a symptom.** A sentence about a subject's "pivotal role in the evolving landscape" is a problem because it says nothing checkable. Swapping "pivotal" for "important" leaves the empty sentence in place. Fix the content, and the wording follows.
4. **The patterns move.** Each model generation has its own habits, and suppressing one habit tends to create another. The em dash is the clearest case: once vendors trained it out, text made only of commas and periods became the new tell.

Strength ratings used below: **strong** (rare in human text, fix on sight), **medium** (common in human text too, judge by density), **weak** (only meaningful alongside other signs).

## 1. Content

The root cause is regression to the mean. A model replaces specific, unusual facts with generic, positive statements that could apply to almost anything. "Inventor of the first train-coupling device" becomes "a revolutionary titan of industry": less specific and more exaggerated at once.

| Pattern | Words to watch | Era | Strength | Fix |
|---|---|---|---|---|
| **Inflated significance, legacy, broader trends** (`WP:AILEGACY`, `WP:AITREND`) | stands/serves as, is a testament/reminder, crucial/pivotal/vital/significant/key role or moment, underscores/highlights its importance, reflects broader, symbolizing its enduring/lasting, setting the stage for, marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted | 2023 onward; since mid-2026 often paired with a hedge ("this distinction matters because…") | strong | Delete the claim, or replace it with the specific fact that would justify it. Mundane facts (population figures, etymology) need no significance statement at all. |
| **Notability and media-coverage emphasis** (`WP:OVERATTRIBUTION`) | independent coverage, local/regional/national media outlets, trade publications, cited/featured/profiled in, written by a leading expert | 2025 onward | strong | Say what the source reported. Describing the source's type or reach is filler. |
| **Identification by sources** (`WP:AIDENTIFY`) | records/listings/filings identify [subject] as, was identified by [source] as, is listed in, his professional profile lists | common from 2026 | strong | State the fact directly and cite it: "He is a retired IAS officer", with the citation carrying the sourcing. |
| **Online-presence filler** | maintains an active social media presence, strong digital presence | 2024 to 2025 | medium | Cut unless the presence is itself the point, and then give numbers. |
| **Superficial analysis** (`WP:SUPERFICIAL`) | trailing "-ing" clauses: highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, cultivating, fostering, encompassing, enhancing; valuable insights; align/resonate with | 2023 onward | strong | Cut the clause. If it carries a real claim, give it its own sentence with a subject and evidence. |
| **Vague connection** (`WP:AICONNECT`) | in connection with, connected to, in association with, associated with | common from 2025 to 2026 | medium | Name the relationship: "was CEO of", "taught science at", "funded". |
| **Vague attribution, overgeneralized opinion** (`WP:AIWEASEL`) | industry reports, observers have cited, experts argue, some critics argue, several sources (when one is cited), "such as" before a list that is actually complete | 2023 onward | strong | Name who said it, or cut it. One reviewer is "one reviewer", never "critics". |
| **Challenges and future-prospects formula** (`WP:FACESCHALLENGES`) | Despite its [praise], [subject] faces several challenges…; Despite these challenges; Future Outlook | 2023 onward | strong | The tell is the rigid formula that ends on a vaguely hopeful note. Report specific problems where they belong in the text, and drop the closing reassurance. |
| **"Awards and recognition" and "X and Y" headings** | Awards and recognition, Challenges and legacy | 2024 onward | weak | Use a heading that names what the section contains. |
| **Promotional tone** (`WP:AIPUFFERY`) | boasts a, vibrant, rich, profound, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking, renowned, diverse array | 2023 to 2025; rare in newer models unless requested | medium | Replace the adjective with the fact it gestures at, or cut it. |

## 2. Language and grammar

| Pattern | Words to watch | Era | Strength | Fix |
|---|---|---|---|---|
| **AI vocabulary** (`WP:AIVOCAB`) | See the era table below | shifts with each model | medium alone, strong in clusters | Use the plain word. Take the list literally: a flagged word's synonyms are not flagged, and "underscore" for an actual underline is fine. |
| **Copula avoidance** (`WP:AINOCOPULA`) | serves as, stands as, marks, functions as, operates as, represents; boasts, features, maintains, offers (meaning "has"); refers to (in an opening definition); holds the distinction of being; ventured into X as; began his career as | 2023 onward | medium | Write "is", "are", "has", "was". |
| **Negative parallelism: not just X, but Y** (`WP:AIPARALLEL`) | not only… but also, it is not just…, it's… | 2023 onward | medium | State Y. Keep the contrast only when a reader would really assume X. |
| **Negative parallelism: not X, but Y** | it's not…, it's…; no…, no…, just… | 2025 onward | medium | Same. |
| **Negative parallelism: Y rather than X** | rather than, instead of | especially 2026 | medium | Same. This reversed form is the current default, and it also carries the mid-2026 source disclaimers in section 3. |
| **Rule of three** (`WP:RO3`) | three adjectives, three short phrases, three parallel clauses | 2023 onward | medium; strong in places nobody bothers with flourish, such as commit messages | Count the real items. If there are three, list three. If the third was added for rhythm, drop it. |
| **Elegant variation** (`WP:AIELEVAR`) | the same thing renamed in each sentence ("constraints", "confines", "norms") | older models; historical | weak | Pick one term and repeat it. Note that some writers, including many non-native English speakers, were taught to avoid repetition. |
| **Title treated as a proper noun** | an opening sentence that defines a descriptive title as if it were a named entity | 2024 to 2025 | weak | Open with the subject matter itself. |

### AI vocabulary by era

| Era | Model generation | Overused words |
|---|---|---|
| 2023 to mid-2024 | GPT-4 | additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate/intricacies, interplay, key, landscape, meticulously, pivotal, underscore, tapestry, testament, valuable, vibrant |
| Mid-2024 to mid-2025 | GPT-4o | align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant |
| Mid-2025 to mid-2026 | GPT-5 | emphasizing, enhance, highlighting, showcasing, plus the notability and media-coverage phrases in section 1 |
| Mid-2026 onward | GPT-6 | challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally; many more periods and commas; sentences held to roughly 8 to 20 words |

Also listed without an era: deep dive, robust. Grok overuses "scientific" words (causal, empirical, correlate) and still overuses "underscore" in 2026.

Several of the mid-2026 words (challenge, matters, practical, steady, clearer) are ordinary English. They are only informative in a cluster, and `humanizer_audit.py` deliberately does not flag them one at a time.

## 3. Communication meant for the chatbot's user

These are leftovers of the conversation, pasted along with the content. All are **strong**: delete on sight.

| Pattern | Words to watch | Fix |
|---|---|---|
| **Collaborative chatter** (`WP:CERTAINLY`) | Of course!, Certainly!, You're absolutely right!, I hope this helps, Would you like…, let me know, is there anything else, here is a…, a more detailed breakdown, check/verify/confirm… before publishing | Delete. Also check HTML comments, where newer models leave drafting notes. |
| **Didactic disclaimers** (`WP:DIDACTIC`) | it is important to note, it is worth noting | Delete the framing and keep the fact, if there is one. |
| **Missing-source disclaimers** (`WP:AIDISCLAIMER`) | while specific details are limited/scarce, not widely available/documented/disclosed, in the provided/available sources, based on available information, maintains a low profile, keeps personal details private | Delete. These are guesses about the model's own search results, presented as facts about the world. Whatever "likely" follows them is speculation. |
| **Corrective framing** (mid-2026 onward) | [claim] should be treated/presented as… rather than…, does not by itself establish, should not be confused with | Delete, or state the limitation once as a plain fact. Nearly unknown before July 2026. |
| **Knowledge-cutoff statements** (`WP:AICUTOFF`) | as of my last knowledge update, up to my last training update | Delete. Historical (2022 to 2023). |
| **Refusals** | as an AI language model, as a large language model, I'm sorry, I cannot… but I can | Delete. Historical. |
| **Placeholders** (`WP:AIPLACEHOLDER`) | [Entertainer's Name], [Year], (Add your channel URL here), Evidence to be supplied: […], `2025-XX-XX`, `INSERT_SOURCE_URL`, `https://example.com/source1` | Fill with the real value or remove the sentence. Never invent the value. |
| **Section summaries** (`WP:CONCLUSION`) | In summary, In conclusion, Overall, a "Conclusion" heading that restates the piece | Delete. Historical in long-form output but still common. End on the last piece of content. |

## 4. Style and markup

| Pattern | Strength | Fix |
|---|---|---|
| Title Case In Section Headings | weak outside Wikipedia (many style guides require it) | Follow the house style. |
| Heavy boldface in running prose | medium | Remove emphasis that does not help someone scanning. |
| Inline-header vertical lists (`- **Label**: explanation`) | medium | Turn into prose, or a real table if the content is tabular. |
| Emoji at the start of headings or list items | strong | Remove. |
| Curly quotes and apostrophes | weak (word processors add them too) | Match the destination's convention. |
| Em dashes (`WP:AIDASH`) | historical since September 2026 | See the note below. |
| Markdown in a non-Markdown destination: `**bold**`, `#` headings, `---` rules, `[text](url)`, fenced blocks labelled with the target format | strong | Convert to the destination's markup. |
| Leaked citation machinery: `contentReference[oaicite:1]`, `↩`, `utm_source=chatgpt.com`, `utm_source=openai`, `utm_source=copilot.com`, `referrer=grok.com` | strong (the URL parameters prove a chatbot found the link, though not that it wrote the prose) | Strip the artifact. Then open the link and check it supports the sentence. |
| Wrong heading levels: a level-1 heading for the title inside a page that already has one, or several level-1 headings | medium | Fix the hierarchy. |

**The em dash note.** Models used em dashes far more than non-professional human writers, usually with spaces around them and usually to punch up a clause. From late 2025 vendors suppressed them, and by September 2026 the newest models avoid them entirely. The side effect is prose with no punctuation except commas and periods, which the source page now lists as its own sign. Neither extreme is the goal. Use the mark the sentence needs: a colon to introduce, parentheses for an aside, a semicolon between related clauses, an occasional dash.

## 5. Citations

Style edits cannot fix these, and they matter more than everything above. A humanized paragraph with a fabricated reference is worse than an awkward paragraph with a real one.

| Sign | What to do |
|---|---|
| Several dead links that were never archived (`WP:AIFICTREF`) | Open each link. Remove claims whose source cannot be found. |
| ISBN with a bad checksum, DOI that does not resolve | Treat the reference as fabricated until shown otherwise. |
| DOI that resolves to an unrelated paper | Same. Check the title, authors, and date against the DOI record. |
| Book citation with no page number or URL, or a page that does not contain the claim | Find the page or flag the claim as unverified. |
| Reference syntax misused, or named references defined but never cited (`WP:AICITESTYLE`) | Rebuild the references and confirm each one supports the sentence it is attached to. |
| Placeholder dates and URLs in citation fields | Fill from the real source or remove. |

A humanizing pass must never add, complete, or "repair" a citation from memory. Flag it for the author.

## 6. Summaries of changes (commit messages, edit summaries, PR descriptions)

`WP:AISUMMARY`. The more a summary follows these formulas, the stronger the sign.

| Pattern | Words to watch | Human equivalent |
|---|---|---|
| Canned assurance of compliance | ensured that… adheres to, refined, enhanced, enriched, streamlined, improved clarity/flow/readability, in compliance with guidelines, neutral tone | Name the one thing changed and why: "removed excessive links per MOS:OVERLINK". |
| Reporting what was not changed | preserved, retained, avoided, ensured, aimed to; "…while preserving the original meaning" | Describe only what changed. |
| Emphasis on sourcing over content | added sourced content, added verified information, improved attribution, with independent/secondary sources | Say what the new content is: "added info about the artist's debut". |
| Itemized parameter and template names | lists of field names, markup quoted in the summary | Summarize at the level a reader cares about. |
| Stating the obvious | addressing reviewer feedback | Say which feedback. |
| Stacked improvements | five kinds of improvement across unrelated areas in one summary | One change per commit, or a short honest list. |

Abbreviations and shorthand ("ce", "typo", "fix link") are signs of a human.

## 7. Comments and discussion replies

`WP:AICOMMENT`. Chatbot replies tend to sound like a customer-service clerk: having "carefully reviewed" something, apologizing for inconvenience they "may have" caused, and promising "if there are specific issues, please point them out and I will resolve them." They also tend to be long, split into titled sections, cite rules that do not exist, and ask the other party to say exactly what should be improved. Fix: answer the actual point in a few sentences, in the first person, and check any rule you cite.

## 8. What human writing has

`WP:HUMANSIGNS`. Observed to be more common in human-written articles than in AI text:

- Simple is/has phrases: "there is a", "it has a".
- Plain words where a stiff synonym exists: wrote (authored), moved (relocated), used (utilized), tried (attempted), died (passed away).
- Superlative or definitive statements where true: "one of the best", "is the only", "was the first". Models avoid these and reach for vague praise.
- Qualifiers and intensifiers: very, perhaps, tends to.
- The occasional wordy construction: as a result of, in order to, all of the, a part of, the fact that.

Two caveats. These describe a population of texts, so they do not license sprinkling "very" and "the fact that" into every paragraph. And none of them is a typing error. The page lists no evidence that typos, dropped articles, or slang mark text as human, and adding them deliberately makes writing worse for the reader.

## 9. Signs that do not work

Do not "fix" these, and do not treat them as evidence of anything:

- **Perfect grammar.** Many people write well.
- **Mixed casual and formal register.** Common among technical writers and in text with several authors.
- **"Bland" or "robotic" prose.** AI text skews positive and verbose, which is a different thing.
- **Formal or academic vocabulary in general.** Only specific words are overused.
- **Transition words in isolation.** Only a few are overused, and style guides accept them.
- **Missing citations.** Modern chatbots add citations freely. The question is whether they are real.
- **Odd or correct markup.** Neither is informative.

## 10. Limits

- Detection tools beat chance but have real error rates, and they are sensitive to paraphrasing, markup, spacing, and models they were not trained on. A detector score is not a measure of writing quality and should not be the target of an edit.
- People are poor judges too. In the studies the source page cites, typical readers did no better than chance, while people who use chatbots heavily for writing identified about 90% of AI text.
- Human writing is drifting toward these patterns as people read more chatbot output, so the catalog will produce more false positives over time.
- Each model has its own idiolect. Broader-context filler is more typical of ChatGPT and Grok, and Gemini and Claude tend to be more concise. Em dashes survived longest in Claude.
- The catalog covers informational prose. Fiction has its own tells, which the source page deliberately leaves out.
