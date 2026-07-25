# Gemini Rue — Simplified Chinese Localization Patch

[中文](README.md) | [![Release](https://img.shields.io/github/v/release/BebopSpikeSpiegel/gemini-rue-chinese-localization?include_prereleases)](https://github.com/BebopSpikeSpiegel/gemini-rue-chinese-localization/releases)

An unofficial Simplified Chinese localization for *Gemini Rue* (Wadjet Eye Games, 2011) — the rain-soaked cyberpunk noir adventure about memory and identity, with Cowboy Bebop in its DNA. A game Chinese-speaking players have waited fifteen years for. Now it speaks Chinese.

![Main menu](assets/menu.png)

## Supported version

- **Steam release (2026 AGS 3.6.1 rebuild)** — the patch is built and tested against it
- Older GOG / retail builds use a pre-Unicode engine and are **not supported**

## Installation

1. Download the latest `GeminiRue-SChinese-*.zip` from [Releases](https://github.com/BebopSpikeSpiegel/gemini-rue-chinese-localization/releases)
2. Extract everything into the game root (`Steam\steamapps\common\Gemini Rue\`, next to `Gemini Rue.exe`) — 5 game files: `SChinese.tra` + `agsfnt3.ttf`–`agsfnt6.ttf`
3. Enable it (either way):
   - edit `acsetup.cfg`: under `[language]` set `translation=SChinese`
   - or change `translation=German,Polish` to `translation=German,Polish,SChinese` in `.config`, then pick SChinese in the `winsetup.exe` language dropdown
4. Launch the game

**Uninstall**: delete those 5 files and clear the `translation=` line. Saves are unaffected.

## Coverage

- All **5,973 lines** of game text: dialogue, narration, terminal databases, newspapers, diaries, UI, key prompts, developer commentary and blooper mode
- **32 achievement-screen strings** (a blind spot even the official German/Polish translations don't cover — recovered from game data for this patch)
- Pixel-art CJK fonts (Fusion Pixel Font) rendered at the game's native resolution

## Known limitations

- List-control items (terminal search results, achievements list) are engine-level AGS ListBoxes that bypass translation lookup and remain English (same in the official German/Polish translations)
- Voice acting remains the English original (text-only localization)
- Terminal searches require English keywords (`Matt`, `kudan`, `Carbon`, …), as in the original

## Building from source

```
python tools/build_tra.py        # source/SChinese.trs -> dist/SChinese.tra
```

`source/SChinese.trs` is the single source of truth (English/Chinese line pairs, UTF-8). `tools/tra.py` implements the AGS 3.6.1 TRA format (verified byte-identical round-trips against the official .tra files). Fonts are not committed — CI bundles a pinned [Fusion Pixel Font](https://github.com/TakWolf/fusion-pixel-font) release at build time.

## AI disclosure

This patch was produced with an **AI bulk translation + human-in-charge** hybrid workflow. In full honesty:

**Tools & models**: Anthropic Claude Code. Reverse engineering, tooling, orchestration and QA by Claude Fable 5; the translation itself by **144 Claude Opus 4.8 agents** — the script split into 72 chunks, each passing a translate → independent-review two-stage pipeline, governed by a translation bible (full plot with spoiler-discipline rules for the twist, per-character voice specs, a locked glossary, and hard mechanical constraints such as voice-sync markers). Followed by programmatic per-line validation (markers / line breaks / format tokens) and a global consistency sweep (zero glossary drift, duplicate-take alignment).

**What did I do**: initiated and directed the project; made every naming and style decision across two checkpoints (transliteration scheme, Latin codenames, terminology, UI labels — all human calls); native-speaker line-by-line review and feedback; on-device playtesting and bug reports; final editorial responsibility.

**What the AI did**: reverse-engineered the TRA binary format and wrote the compiler; validated the font-replacement approach; drafted the story bible and glossary; produced and cross-reviewed the 5,973-line translation; ran mechanical validation and consistency sweeps; excavated and translated the achievement strings from game data.

Found a translation issue? Please open an [Issue](https://github.com/BebopSpikeSpiegel/gemini-rue-chinese-localization/issues) with a screenshot and where it occurs.

## Acknowledgements

- **Joshua Nuernberger** and **Wadjet Eye Games** — for the masterpiece, and for still maintaining it fifteen years on. If you'd ever like to adopt this translation officially, the license explicitly allows it (see below)
- **TakWolf**'s [Fusion Pixel Font](https://github.com/TakWolf/fusion-pixel-font) (SIL OFL-1.1)
- The Adventure Game Studio engine and community
- Anthropic Claude

## License

See [LICENSE](LICENSE). In short:

- Everyone may copy, redistribute and modify this patch freely, **non-commercially**, with attribution
- **Original-author grant**: Wadjet Eye Games, LLC and Joshua Nuernberger receive a perpetual, royalty-free, irrevocable license for any commercial use — including adopting this translation as the official Chinese localization
- The original game text remains the property of its copyright holders; the English source strings included here are a technical necessity of the .tra key-value mechanism; takedown honored on request
- Fonts are separately licensed under the [SIL OFL-1.1](THIRD_PARTY/OFL.txt)
