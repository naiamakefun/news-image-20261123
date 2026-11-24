# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/naiamakefun/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/naiamakefun/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

**THE MONDAY EDITION** — the whole of Monday 23 November 2026 on one broadsheet page.

Fifty stories that happened, or were first reported, on that single Monday, drawn as a
newspaper front page. Fourteen numbered panels carry the day's biggest stories, each with
its own drawn scene (no photographs, no icons): Democrats clinching their largest House
majority since 1992, Asia's AI sell-off entering a second week, Belgium's airports shut by
a national strike, an Oxfam report finding contamination indicators across 99% of Gaza,
Reuters counting DR Congo's graves to show the Ebola toll is far above the official count,
the NHS launching the world's largest AI breast-cancer screening trial, Indonesia
confirming 24 dead in the Cikande candy-factory fire, a robot sub finding the deepest
explosive volcanic deposits ever recorded near Challenger Deep, Nepal's PM Balen Shah
welcomed in Delhi, Shuri Castle's red hall reopening seven years after the fire, a deep
M6.5 earthquake off Vanuatu, FIFA set to confirm the UK as 2035 Women's World Cup host,
bomb-threat emails sparking evacuations at some 450 schools across Germany, and the US Army preparing to
detonate unstable explosives in Iowa despite a court order.

A further 36 stories run in the "Also on Monday" columns, a pinned world map shows where
the 14 numbered stories happened, and a DATE CHECK box names the big stories deliberately
left out because they belong to other days (COP31's gavel fell on Sunday; the Shenzhen
summit was Thursday). Every panel is tagged CONFIRMED or REPORTED with its source outlet,
so nothing on the page claims more than the reporting supports.

The image is generated entirely in code: `build_image.py` draws every panel, vignette,
map pin and column with Pillow and writes `entry.png` (1024 × 1024). `main.ts` is the
runtime entrypoint — it copies the committed `entry.png` into `$MAKEFUN_OUTPUT_DIR`
(default `/output`), creating the directory if needed, and verifies the copy.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To rebuild the picture itself: `python3 build_image.py` (requires Pillow).

---
<sub>Entered on [make.fun](https://make.fun/?ref=naia&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
