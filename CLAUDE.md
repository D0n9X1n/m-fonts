# CLAUDE.md — m-fonts

m-fonts builds two font families from Recursive, Resource Han Rounded, and Nerd
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
  only its name and `Mono: false`; keep it that way unless asked otherwise.
- Upstream versions live only in `versions.env`. Never vendor upstream fonts or
  the Nerd Fonts patcher into the repository; `sources/` is fetched and ignored.
- Python dependencies are pinned exactly in `requirements.txt`.
- Workflow actions are pinned to commit SHAs with a trailing `# vX.Y.Z` comment.

## Commands

```bash
./scripts/local-gate.sh            # fast checks: scripts, configs, wiki, release notes
./scripts/local-gate.sh --build    # plus a full build and font verification
./scripts/check-updates.sh         # compare versions.env with upstream releases
```

Run `./scripts/local-gate.sh --build` before opening a pull request that changes
font output.
