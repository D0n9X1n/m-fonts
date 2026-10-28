# CLAUDE.md — Rec Mountain Fonts

Rec Mountain Fonts builds two font families from Recursive, Resource Han Rounded, and Nerd
Fonts: **Rec Mono St.Helens** (monospace, for code) and **Rec Sans Mt.Baker**
(proportional, for text). Both share one design.

## Read first

- [`wiki/Configuration.md`](wiki/Configuration.md) — family configs, `Extends`, pinned upstream versions.
- [`wiki/Build-Pipeline.md`](wiki/Build-Pipeline.md) — the four build stages and the verifier.
- [`wiki/Release-Process.md`](wiki/Release-Process.md) — CI, tag-driven releases, version numbers.
- [`wiki/Wiki-Publication.md`](wiki/Wiki-Publication.md) — documentation rules.

**Canonical documentation rule:** `wiki/` is the only documentation surface.
Each topic has an English `wiki/<Page>.md` and a Chinese `wiki/<Page>-zh-CN.md`
with matching heading structure and equivalent facts; update both in the same
change. Load only the English files for routine context. Verify descriptions
against the current scripts and configs before writing them.

## Rules

- `configs/st-helens.yaml` is the shared design. Mt.Baker extends it and changes
  only its name, `Mono: false`, and `Exclude Features: [ss10]` (plain zero); keep
  it that way unless asked otherwise.
- Upstream versions live only in `versions.env`. Never vendor upstream fonts or
  the Nerd Fonts patcher into the repository; `sources/` is fetched and ignored.
- Python dependencies are pinned exactly in `requirements.txt`.
- Workflow actions are pinned to commit SHAs with a trailing `# vX.Y.Z` comment.
- The preview images in `README.md` and `wiki/Fonts*.md` come from
  `docs/previews/`. After any change to fonts, configs, or
  `scripts/render-previews.py`, rebuild, run `python3 scripts/render-previews.py`,
  look at every changed image, and commit them in the same change. Every
  preview must appear in `README.md`; the local gate checks this.

## Commands

```bash
./scripts/local-gate.sh            # fast checks: scripts, configs, wiki, release notes
./scripts/local-gate.sh --build    # plus a full build and font verification
./scripts/check-updates.sh         # compare versions.env with upstream releases
```

Run `./scripts/local-gate.sh --build` before pushing a change to font output.
