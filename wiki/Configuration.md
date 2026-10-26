# Configuration

[简体中文](Configuration-zh-CN)

Each family is one YAML file in `configs/`. Upstream versions live in
`versions.env`.

## Family configs

`configs/st-helens.yaml` holds the shared design:

| Key | Meaning |
|---|---|
| `Family Name` | Full family name, for example `Rec Mono St.Helens`. File and PostScript names drop the spaces. |
| `Mono` | `true` builds a monospace family (`MONO 1`); `false` builds a proportional one (`MONO 0`) |
| `Styles` | `CASL`, `wght`, `slnt`, and `CRSV` for each of Regular, Italic, Bold, and Bold Italic |
| `Code Ligatures` | Turn Recursive's code ligatures on by default. Applied to mono families only. |
| `Features` | Stylistic sets frozen into the fonts |

`configs/mt-baker.yaml` starts from St.Helens:

```yaml
Extends: st-helens.yaml

Family Name: Rec Sans Mt.Baker
Mono: false
```

`Extends` loads the named file first; keys in the extending file replace the
parent's. Any change to St.Helens's styles or features therefore applies to
Mt.Baker too.

## Code ligatures

Recursive draws code ligatures as glyphs wider than one cell. For a mono family
the build gives each one a single-cell advance and shifts its outline left so it
overhangs the cells before it. In a proportional family that would squash every
glyph wider than a space, so the build skips ligatures when `Mono` is `false`,
even if `Code Ligatures` is `true`.

## Stylistic sets

| Feature | Change | Applies to |
|---|---|---|
| ss01 | Single-story a | Roman only |
| ss02 | Single-story g | Roman only |
| ss03 | Simplified f | Roman only |
| ss04 | Simplified i | Roman only |
| ss05 | Simplified l | Roman only |
| ss06 | Simplified r | Roman only |
| ss07 | Simplified italic diagonals (kwxyz) | Roman and cursive |
| ss08 | Serifless L and Z | Roman and cursive |
| ss09 | Simplified 6 and 9 | Roman and cursive |
| ss10 | Dotted 0 | Roman and cursive |
| ss11 | Simplified 1 | Roman and cursive |
| ss12 | Simplified @ | Roman and cursive |

## Upstream versions

`versions.env` pins each upstream release:

```bash
RECURSIVE_VERSION=1.085
RESOURCE_HAN_ROUNDED_VERSION=0.990
NERD_FONTS_VERSION=3.5.1
```

`./scripts/check-updates.sh` compares these with the latest GitHub releases,
ignoring pre-releases, and exits 1 if any is behind. To update one, change the
version, also update the version badges in `README.md` and the block above in
both Configuration pages (the local gate fails until they match), run
`./scripts/local-gate.sh --build`, and check the result in an editor before
merging.

## Adding a family

1. Add `configs/<name>.yaml`, usually with `Extends: st-helens.yaml`.
2. Run `./scripts/build.sh configs/<name>.yaml`.

`build-all.sh`, the verifier, CI, and release packaging pick up every file in
`configs/` automatically.
