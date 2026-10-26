# Fonts

[简体中文](Fonts-zh-CN)

m-fonts ships two families that share one design. St.Helens is for code; Mt.Baker
is the same letterforms with natural widths for everyday text.

## Preview

### Styles

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/D0n9X1n/m-fonts/main/docs/previews/styles-dark.png">
  <img alt="Regular, Italic, Bold, and Bold Italic of both families" src="https://raw.githubusercontent.com/D0n9X1n/m-fonts/main/docs/previews/styles-light.png" width="800">
</picture>

### Code

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/D0n9X1n/m-fonts/main/docs/previews/code-dark.png">
  <img alt="TypeScript in Rec Mono St.Helens with code ligatures and italic keywords" src="https://raw.githubusercontent.com/D0n9X1n/m-fonts/main/docs/previews/code-light.png" width="800">
</picture>

### Terminal

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/D0n9X1n/m-fonts/main/docs/previews/terminal-dark.png">
  <img alt="A shell prompt with Powerline segments, Nerd Font icons, and a CJK table aligned on the cell grid" src="https://raw.githubusercontent.com/D0n9X1n/m-fonts/main/docs/previews/terminal-light.png" width="800">
</picture>

### Ligatures

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/D0n9X1n/m-fonts/main/docs/previews/ligatures-dark.png">
  <img alt="Thirty code ligatures in Rec Mono St.Helens" src="https://raw.githubusercontent.com/D0n9X1n/m-fonts/main/docs/previews/ligatures-light.png" width="800">
</picture>

### Text

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/D0n9X1n/m-fonts/main/docs/previews/text-dark.png">
  <img alt="English, Chinese, and Japanese paragraphs in Rec Sans Mt.Baker" src="https://raw.githubusercontent.com/D0n9X1n/m-fonts/main/docs/previews/text-light.png" width="800">
</picture>

### Glyph coverage

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/D0n9X1n/m-fonts/main/docs/previews/glyphs-dark.png">
  <img alt="Glyph coverage: Latin, Vietnamese, mathematical Greek, CJK, kana, box drawing, Powerline, and Nerd Font icons" src="https://raw.githubusercontent.com/D0n9X1n/m-fonts/main/docs/previews/glyphs-light.png" width="800">
</picture>

## Families

| Family | Use | Spacing | Code ligatures |
|---|---|---|---|
| **Rec Mono St.Helens** | Editors and terminals | Monospace, 600-unit cell | Yes |
| **Rec Sans Mt.Baker** | Documents and UI | Proportional | No |

Each family has four styles: Regular, Italic, Bold, and Bold Italic.

## Shared design

Both families come from one config (`configs/st-helens.yaml`); Mt.Baker changes
only its name and spacing. See [Configuration](Configuration).

| Setting | Value |
|---|---|
| Casual (`CASL`) | 1 — the casual, brush-like Recursive design |
| Cursive (`CRSV`) | 1 — cursive letterforms |
| Slant (`slnt`) | -4° for Regular and Bold, -10° for Italic and Bold Italic |
| Weight (`wght`) | 400 for Regular and Italic, 600 for Bold and Bold Italic |
| Stylistic sets | ss01–ss12, including the dotted zero (ss10) |

Recursive's ss01–ss06 alternates apply only to Roman (`CRSV 0`) glyphs, so they
have no visible effect with `CRSV 1`. They stay in the config so a Roman family
can reuse it.

## Glyph coverage

| Source | Coverage |
|---|---|
| Recursive | Latin (including Vietnamese), 20 mathematical Greek letters, box drawing, blocks, punctuation, and symbols. No Cyrillic. |
| Resource Han Rounded CN | CJK ideographs (20,976 in U+4E00–9FFF), kana, CJK punctuation, full-width and halfwidth forms |
| Nerd Fonts | Every icon set the patcher's `--complete` option adds, including Powerline |

CJK glyphs come from Resource Han Rounded's Regular weight for Regular and
Italic, and its Bold weight for Bold and Bold Italic. They are scaled 1.15×
relative to Recursive's line height. Hangul syllables are not included.

## Spacing differences

| Glyph group | St.Helens | Mt.Baker |
|---|---|---|
| ASCII | Always 600 | Natural width (for example `i` 350, `m` 850) |
| CJK and full-width forms | 1200 (two cells) | Scaled source width (1150) |
| Halfwidth forms | 600 (one cell) | Scaled source width (575) |
| Nerd Font icons | Two cells, centred | Natural width |
| Code ligatures (`=>`, `!=`) | On by default | Off |

St.Helens also sets the flags Windows Terminal and DirectWrite need to keep
ASCII text on the cell grid; see [Build Pipeline](Build-Pipeline).
