# Project README contract

Every repo published from this profile gets a README built to this contract. A task brief names the repo, its facts and its scrub list. This file holds what is the same for all of them.

## Who reads it

1. A person with 30 seconds: a recruiter or an engineer deciding whether to keep reading.
2. An AI agent told "install this and run it".

The top of the file serves the person. `## Run it` serves the agent. Neither reader should need the other's part.

## Sections, in this order

1. **Title and one sentence.** `# name`, then what the project is in plain words. No adjectives.
2. **Status.** Directly under the sentence: `**Status: work in progress.**` followed by one sentence on what works today and one on what does not exist yet. Take both from the roadmap, the handoff notes and the tests. Do not guess.
3. **Hero visual.** One image or one short loop. Leave it out when the project has nothing visual.
4. **`## What it is`.** Two to four short paragraphs: the problem, who it is for, what it does. First person is fine when the repo's docs record the reason ("I built this because").
5. **`## What works today`.** A list. Each item is something a user can do now, with its evidence: a command, a test, a screenshot. Close with `### Next`, three to five items from the roadmap.
6. **`## Look`.** Only for repos with visuals. A gallery with a caption per image saying what it shows. Alt text on every image.
7. **`## Run it`.** See the next section.
8. **`## How it's built`.** One mermaid diagram of the real components and the data that moves between them, 12 nodes at most. Then a repo map table, path and what lives there, 10 rows at most.
9. **`## Why it's built this way`.** See below.
10. **`## How it was made`.** Optional, four sentences at most: specs, tickets, gated agent runs in Claude Code, review by the owner. Link `CLAUDE.md` and `docs/adr`. No model names, account names, plan names or billing details.
11. **`## Credits and licence`.** Third-party code, assets and fonts with their licences. Any required disclaimer. MIT, `Copyright (c) 2026 Kevin Shibuya`, and add the `LICENSE` file when it is missing.

## Run it

Write this section so an agent can execute it top to bottom without reading anything else.

- Open with a facts table: runtime and version, package manager and version, operating system limits, external services, paid keys needed (yes or no, and which), ports used, time to first run.
- Then numbered steps. Each step is one fenced command block with no `$` prompt, followed by one line starting `Expect:` that says what the reader sees when it worked.
- `### Check it works`: the test command and the summary line a passing run prints.
- `### Environment variables`: a table of name, required or optional, what it does, how to get a value. Never a real value.
- `### If it fails`: up to three failure and fix pairs, only ones the repo's docs record.
- One line for agents: where the repo's working rules live (`CLAUDE.md` or `AGENTS.md`).

You run every command yourself on a clean checkout before it goes in. A command you could not run is marked `Not run here:` with the reason.

## Why it's built this way

Four to eight decisions. Each one:

- Opens with the decision as a bold sentence ending in a period.
- Then two to four sentences: what forced it (the incident, the measurement or the constraint, as the record states it), what was rejected, what it costs.
- Links the ADR, spec or doc it comes from.

Only decisions the repo records. Quote numbers exactly. When the record gives no reason, leave the decision out. Prefer the decisions with a story: a failed first attempt, a measured bake-off, a manual pass that found the flaw.

## Writing

- Run the `unslop` skill over every line of public text, the PR body included.
- Sentence-case headings. No emoji. No em dashes. No badges.
- A number beats an adjective. A sentence that could sit unchanged in another project's README gets cut.
- English. 150 to 300 lines.

## Images

- They live in `docs/readme/`.
- PNG or WebP for stills, 500 KB each at most. GIF or animated WebP for loops, 3 MB at most.
- Screenshots: 1280 px wide viewport at 2x, cropped to the subject. Use the dark theme when the app has both.
- Pixel art blurs when GitHub scales it. Upscale copies by a whole-number factor with nearest-neighbour sampling.
- Commit the script that takes the screenshots so they can be regenerated.
- No browser opens outside `heavy browser:1 -- <cmd>`. No dev server starts except through `devserve run --port <N> -- <cmd>`.
- Only images the owner made or the project generated. No third-party screenshots, logos or art.

## Must never appear

In the tree, the README, commit messages you write, or the PR text:

- Employer, team, client, partner, co-founder or friend names.
- Account names, plan names, quota or billing details.
- Server names, IP addresses, SSH key names, home-directory paths.
- Details of repos that stay private.
- Phone numbers. Email addresses other than `hello@kevinshibuya.com`.

Session notes (`HANDOFF*.md`) leave the tree. The task brief gives the exact pattern to grep for.

## Gate

Report each line with its command and exit code.

1. `gitleaks git . --redact --no-banner` shows no finding beyond the false positives the brief lists.
2. The forbidden-pattern grep over the tree comes back empty.
3. Issue and PR text scan. Dump every issue and PR title, body and comment with `gh` to a file outside the repo. Grep it with the forbidden pattern, an email pattern and `/Users/`. Report the hits by issue or PR number and kind. Edit nothing.
4. The repo's own cheap checks pass: lint, typecheck, and the tests for files you changed.
5. Every relative link and image path in the README exists.

## Deliver

- Branch `docs/public-readme` from the staging branch (`.claude/staging`, or `ai-staging` when the repo has no such file).
- One PR into the staging branch, body in the `pr` shape: what to test by hand, what you verified yourself.
- Then stop. Do not merge. Do not change visibility, description, topics or the default branch. Do not edit or close issues. Do not push to `main`.

## Report back

- PR URL and head SHA.
- The gate lines.
- A proposed GitHub description, 120 characters at most, and up to eight topics.
- Anything that should block publishing.
- What you could not verify.
