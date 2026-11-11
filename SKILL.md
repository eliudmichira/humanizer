---
name: humanizer
description: Rewrites prose so it reads as written by a person who knows the subject, removing the patterns catalogued in Wikipedia's "Signs of AI writing" (inflated significance, vague attribution, chatbot residue, formulaic structure, AI vocabulary) while keeping every fact, number, quote, and technical token intact. Use when asked to humanize, de-slop, or edit text that "sounds like ChatGPT", when reviewing a draft for AI tells, or as a final pass on articles, docs, emails, marketing copy, commit messages, and PR descriptions. Has a detect-only mode.
---

# Humanizer

Edit prose so that a reader gets specific, checkable statements in plain language, in the author's own voice.

The pattern catalog comes from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). The full table, with word lists, dates, and strength ratings, is in `docs/wikipedia_tells.md`. Read it when you need to look up a pattern. The rules below are enough for most edits.

## What this skill is for

It improves writing for the people who will read it. It is an editing pass on a draft the author is entitled to publish under their own name.

It does not target AI-detector scores. Detectors have real error rates and are sensitive to trivial changes, so a score says little about quality, and no set of rules can promise one. Never tell the user the output will "pass" a detector. If the destination requires human-written work or disclosure of AI assistance (a class, a journal, a client contract, a rating or annotation job), this skill does not change that obligation, and you should not help disguise authorship: no deliberate typos, no dropped words, no invented personal experience.

## Hard rules

These override every stylistic rule below.

1. **Keep the meaning.** Every claim in the output must be in the input. Do not add facts, examples, statistics, quotes, sources, anecdotes, or opinions. Do not strengthen or weaken a claim.
2. **When a sentence is empty, cut it or ask.** Much AI text is vague because the model had nothing specific to say. You cannot fix that by guessing the specifics. Delete the sentence, or keep a plain version and list it under "Needs the author" in your report.
3. **Protect technical tokens.** Copy these character for character: code blocks, inline code, commands, file names and paths, URLs and link targets, numbers and units, dates and timestamps, identifiers, version strings, direct quotations, citations, proper names, and any heading or label the destination format requires.
4. **Never repair a citation from memory.** If a reference looks fabricated (dead link, DOI that points elsewhere, no page number), flag it. Do not complete or replace it.
5. **Keep the format the destination needs.** Markdown stays Markdown, wikitext stays wikitext, a plain-text field gets plain text.

## Process

1. **Read for context.** What kind of document is it, who reads it, and how formal is it? If the user supplied samples of the author's writing, note their sentence length, favorite words, punctuation habits, and how they open and close. Match those. Without samples, aim for clear and plain at the register of the original.
2. **Measure before editing.** If you can run code, run `python humanizer_audit.py --file <path>` for a ranked list of hits. Otherwise scan by hand in the order of the tiers below. If the text is already clean (a couple of weak hits), say so and change little. Rewriting clean text only swaps the author's voice for yours.
3. **Edit in tier order.** Tier 1 is deletion. Tiers 2 and 3 are where the real work is. Tier 4 is cleanup.
4. **Reread the result as a reader would.** Check it against the "Do not overcorrect" list. Check that every protected token survived. Check that no claim was added.
5. **Report.** Give the rewritten text, then a short list of what changed and anything that needs the author.

## The patterns

### Tier 1: remove on sight

These are almost never written by a person on purpose.

- **Chatbot conversation.** "Certainly!", "Of course!", "I hope this helps", "Would you like me to…", "Let me know if…", "Here is a revised version…", "as an AI language model", "as of my last knowledge update". Check HTML comments too.
- **Unfilled placeholders.** `[Company Name]`, `[Year]`, "(add your URL here)", `2025-XX-XX`, `INSERT_SOURCE_URL`, links to `example.com/…`. Never fill these by guessing. Flag them.
- **Leaked machinery.** `contentReference[oaicite:0]`, `↩`, `utm_source=chatgpt.com`, `utm_source=openai`, `utm_source=copilot.com`, `referrer=grok.com`. Strip the tracking parameter and keep the rest of the URL.
- **Markdown in the wrong place.** Asterisks for bold, `#` headings, or `---` rules in a destination that does not render Markdown.
- **Emoji leading headings or bullets**, unless the author's own samples do it.

### Tier 2: content that says nothing

Here the wording is a symptom. The sentence is generic, and the fix is to make it specific or remove it.

- **Inflated significance.** "stands as a testament to", "plays a pivotal role", "marks a key turning point", "reflects broader trends", "in the evolving landscape of", "left an indelible mark". Ask what fact would justify the claim. State that fact if the text contains it. Otherwise cut.
- **Trailing "-ing" analysis.** "…, highlighting its importance", "…, ensuring a seamless experience", "…, reflecting a commitment to quality". Cut the clause. If it holds a real claim, give it its own sentence with a subject.
- **Vague attribution.** "Experts argue", "observers have noted", "industry reports suggest", "several sources" for one source. Name who, or cut.
- **Describing the sources.** "has been featured in regional media outlets", "received independent coverage", "public records identify him as", "her profile lists her as". State the fact and let the citation do the sourcing.
- **Vague connection.** "was associated with the leadership of", "connected with science education at". Name the relationship: "was CEO of", "taught science at".
- **Disclaimers about information.** "While specific details are limited…", "not widely documented", "based on available information", "it is important to note", "X should be treated as Y rather than Z", "this does not by itself establish". Delete. If there is a real limitation, state it once as a fact.
- **The challenges formula.** "Despite its [strengths], X faces several challenges…" closing on an optimistic line. Report the specific problem where it belongs and drop the reassurance.
- **Summary endings.** "Overall,", "In conclusion,", "In summary,", or any closing sentence that restates the piece. End on the last piece of content.

### Tier 3: sentence habits

Judge these by density. One instance is fine. A cluster is the problem.

- **Copula avoidance.** "serves as", "stands as", "functions as", "represents", "boasts", "features", "offers", "holds the distinction of being". Write "is" and "has".
- **Negative parallelism.** "not just X, but Y", "it's not X, it's Y", "Y rather than X", "instead of X". These argue against a view nobody stated. Say Y. Keep the contrast only when a reader would really assume X.
- **Rule of three.** Three adjectives, three phrases, three parallel clauses, used for rhythm. Count the real items. Three real things stay three. A third item added to round out the sentence goes.
- **AI vocabulary.** The words change with each model generation, so check the era table in `docs/wikipedia_tells.md`. Long-running ones: additionally, crucial, delve, enhance, foster, garner, highlight, intricate, landscape, leverage, meticulous, multifaceted, pivotal, robust, showcase, tapestry, testament, underscore, vibrant. Use the plain word. Take the list literally: its synonyms are not on it.
- **Stiff synonyms.** authored, relocated, utilized, attempted, commenced, passed away. Write wrote, moved, used, tried, started, died.
- **Elegant variation.** Renaming the same thing in every sentence. Pick one term and repeat it.
- **Uniform rhythm.** Every sentence between 8 and 20 words, every paragraph the same length, punctuation limited to commas and periods. This is the newest default (mid-2026 models). Let length follow content: a short sentence for a simple point, a long one where the idea has parts. Use colons, parentheses, and semicolons where they fit.

### Tier 4: formatting

- Bold scattered through running prose.
- Bulleted lists where each item is `**Label**: explanation`. Write prose, or a table if the content is tabular.
- Title Case Headings where the house style is sentence case.
- Headings in "X and Y" form that name no content ("Challenges and legacy").
- Em dashes used to punch up a clause, usually with spaces around them. Use a comma, colon, or parentheses where one fits. An occasional dash is fine.
- Curly quotes where the destination uses straight ones.

### Change summaries

Commit messages, PR descriptions, and edit summaries have their own formula: a stack of improvements ("improved clarity, flow, and readability"), an assurance of compliance ("ensured a neutral tone in line with guidelines"), and a report on what was left alone ("while preserving the original meaning"). Write what changed and why, at the level a reviewer cares about. "Fix off-by-one in pagination" is better than any of those.

## What to write instead

These are the features Wikipedia's editors found more often in human-written text.

- Plain "is", "are", "has", "there is".
- The ordinary word.
- Definite statements where the text supports them: "the first", "the only", "one of the largest". Vague praise is what a model writes when it avoids committing.
- Qualifiers that carry real uncertainty: "perhaps", "tends to", "about".
- Specifics: the name, the number, the date, the place.
- Repetition of the right term.
- A first-person view where the genre allows it and the author holds it.

## Do not overcorrect

A rewrite that mechanically removes patterns is as recognizable as the original.

- **No blanket bans.** "Rather than" is correct for a real contrast. "Robust" is a term of art in statistics. "Underscore" is also a character. Three things happened, so the list has three items.
- **Do not trade one tic for another.** Replacing every "Additionally" with "Also", or every em dash with a comma, leaves the same structure with different paint.
- **Do not chop.** A run of short flat sentences is its own machine rhythm, and it is harder to read than the sentence it replaced.
- **Do not fake humanity.** No deliberate typos, dropped articles, forced slang, filler ("kind of", "pretty much"), or invented asides. They make the text worse and misrepresent how it was written.
- **Do not change register.** A legal memo stays formal. A casual post stays casual.
- **Do not edit what is not prose.** Tables of data, code, quoted material, legal boilerplate, and reference lists are left alone.
- **Good formal writing is not an AI tell.** Correct grammar, academic vocabulary in general, and ordinary transition words are not on the list. Leave them.

## Example

Before:

> Founded in 2014, Brightline Coffee stands as a testament to Nairobi's vibrant café culture. The roastery boasts a diverse array of single-origin beans, showcasing its commitment to quality, sustainability, and community. Industry observers have noted its growing influence, highlighting its pivotal role in the evolving specialty-coffee landscape. Despite these successes, Brightline faces several challenges, including rising costs. Overall, it's not just a coffee shop — it's a movement.

After:

> Brightline Coffee is a roastery in Nairobi, founded in 2014. It sells single-origin beans. Its costs are rising.

Needs the author:

- Which observers, and what did they say? Cut as unattributed.
- "Commitment to quality, sustainability, and community": is there a certification, a sourcing policy, a program? Cut as unsupported.
- Which costs are rising, and by how much?

The result is a third of the length because the original contained three facts. That is the honest outcome. Padding it back out with invented detail would break hard rule 1. The author's answers are what make it longer and better.

## Modes

- **Humanize** (default): rewrite, then report.
- **Detect only**: when asked to review or audit, list the patterns found with the quoted text and the tier, most serious first, and change nothing. State plainly that this is a style review and cannot establish who or what wrote the text.
- **Light pass**: when the text is mostly clean or the user asks for minimal changes, fix tier 1 and tier 2 only.

## Output format

1. The rewritten text, in the same format as the input, with nothing before it.
2. **Changes**: three to six bullets naming the main patterns removed.
3. **Needs the author**: claims cut for lack of support, placeholders, and citations that need checking. Omit the section if empty.
