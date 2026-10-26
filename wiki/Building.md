# Building

[简体中文](Building-zh-CN)

The build turns pinned upstream releases into the eight release fonts. It runs
the same way locally and in CI.

## Prerequisites

| Tool | macOS | Debian/Ubuntu |
|---|---|---|
| Python 3 | Included with Xcode tools or Homebrew | `python3`, `python3-venv` |
| FontForge | `brew install fontforge` | `apt-get install fontforge python3-fontforge` |
| 7-Zip | `brew install sevenzip` | `apt-get install p7zip-full` |
| curl, unzip | Preinstalled | Preinstalled |

Python packages are pinned in `requirements.txt`:

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## Build

```bash
./scripts/build-all.sh                       # every family in configs/, in parallel
./scripts/build.sh configs/st-helens.yaml    # one family
./scripts/build-all.sh 1.2                   # override the CJK scale (default 1.15)
```

Output goes to `fonts/<CompactFamily>/`, for example
`fonts/RecMonoSt.Helens/RecMonoSt.Helens-Regular.ttf`. A full build takes about
90 seconds on an Apple Silicon Mac.

## Upstream sources

The first build runs `scripts/fetch-sources.sh`, which downloads the versions
pinned in `versions.env` into `sources/`:

| Directory | Contents |
|---|---|
| `sources/recursive/` | `Recursive_VF_<version>.ttf` and the code-ligature feature file |
| `sources/resource-han-rounded/` | `ResourceHanRoundedCN-Regular.ttf` and `-Bold.ttf` |
| `sources/nerd-fonts-patcher/` | The Nerd Fonts `font-patcher` and its glyph sources |

Each directory records its version in `.version`; later builds skip the download
until `versions.env` changes. `sources/`, `build/`, and `fonts/` are git-ignored.

## Checks

```bash
./scripts/local-gate.sh            # scripts, configs, wiki, release notes (seconds)
./scripts/local-gate.sh --build    # also builds and verifies every family
```

Run the gate before opening a pull request. CI runs the same checks; see
[Release Process](Release-Process).
