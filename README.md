# The World in One Day — Friday 20 November 2026

[![make.fun — news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![Rank](https://make.fun/badge/news-image-20261120/donghua9711-oss/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![Reward](https://make.fun/badge/news-image-20261120/donghua9711-oss/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Output](https://img.shields.io/badge/output-1024%C3%971024%20PNG%20%E2%89%A4%201%20MiB-blue)](entry.png)

One image that sums up the world news of **Friday 20 November
2026**: a one-page newspaper. Thirty-seven verified stories
from seven regions — Shenzhen's four-point declaration
published, Russia's biggest barrage of the year on Kyiv,
GTA VI's $3.79 billion day, the World Court's genocide ruling
shaking Myanmar, Anthropic's debut close amid an AI sell-off,
a Houthi missile in Riyadh, a burning tanker in Hormuz,
COP31's deal-less final day, Kenya's last Ebola patient going
home, Haiti's deadly Martissant raid and a fifth straight
fall on world markets — drawn, mapped and footnoted on a
single page.

## The page

- Navy masthead with the day and a rainbow band of region
  counts, then a "day in UTC" timeline of five grounded
  moments.
- Three lead stories with artwork on top, then eight more
  illustrated cards — eleven drawn stories in all.
- A dot-matrix world map marking where it happened, and the
  remaining twenty-six stories as one-line briefs.
- A date-check footer: everything printed happened, or was
  first reported, on Friday 20 November 2026. Follow-ons are
  framed as follow-ons — the Shenzhen summit and the ICJ
  judgment were Thursday's; Friday carried their texts and
  fallout.

## Run it

```bash
node main.ts
```

Running the program writes
`the-world-in-one-day-2026-11-20.png` — a 1024×1024 PNG
under the 1 MiB cap, byte-identical on every run. The page
itself is composed by `compose.py` from the artwork in
`assets/`; per-story sourcing lives in [SOURCES.md](SOURCES.md).

## License

MIT — see [LICENSE](LICENSE).
