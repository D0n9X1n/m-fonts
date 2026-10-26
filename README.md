# m-fonts

[![CI](https://github.com/D0n9X1n/m-fonts/actions/workflows/ci.yml/badge.svg)](https://github.com/D0n9X1n/m-fonts/actions/workflows/ci.yml)
[![Release](https://github.com/D0n9X1n/m-fonts/actions/workflows/release.yml/badge.svg)](https://github.com/D0n9X1n/m-fonts/actions/workflows/release.yml)
[![Publish wiki](https://github.com/D0n9X1n/m-fonts/actions/workflows/publish-wiki.yml/badge.svg)](https://github.com/D0n9X1n/m-fonts/actions/workflows/publish-wiki.yml)
[![Version](https://img.shields.io/github/v/release/D0n9X1n/m-fonts?sort=semver&label=version)](https://github.com/D0n9X1n/m-fonts/releases/latest)
[![Release date](https://img.shields.io/github/release-date/D0n9X1n/m-fonts?label=released)](https://github.com/D0n9X1n/m-fonts/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/D0n9X1n/m-fonts/total?label=downloads)](https://github.com/D0n9X1n/m-fonts/releases)
[![Stars](https://img.shields.io/github/stars/D0n9X1n/m-fonts?style=flat&label=stars)](https://github.com/D0n9X1n/m-fonts/stargazers)
[![Issues](https://img.shields.io/github/issues/D0n9X1n/m-fonts?label=issues)](https://github.com/D0n9X1n/m-fonts/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/D0n9X1n/m-fonts?label=prs)](https://github.com/D0n9X1n/m-fonts/pulls)
[![Last Commit](https://img.shields.io/github/last-commit/D0n9X1n/m-fonts?label=last%20commit)](https://github.com/D0n9X1n/m-fonts/commits/main)

[![Recursive](https://img.shields.io/badge/Recursive-1.085-blue)](https://github.com/arrowtype/recursive/releases/tag/v1.085)
[![Resource Han Rounded](https://img.shields.io/badge/Resource_Han_Rounded-0.990-blue)](https://github.com/CyanoHao/Resource-Han-Rounded/releases/tag/v0.990)
[![Nerd Fonts](https://img.shields.io/badge/Nerd_Fonts-3.5.1-blue)](https://github.com/ryanoasis/nerd-fonts/releases/tag/v3.5.1)
[![Wiki](https://img.shields.io/badge/docs-wiki-informational)](https://github.com/D0n9X1n/m-fonts/wiki)
[![Font license: OFL-1.1](https://img.shields.io/badge/font_license-OFL_1.1-lightgreen.svg)](https://openfontlicense.org)
[![Script license: MIT](https://img.shields.io/badge/script_license-MIT-blue.svg)](LICENSE)

Two font families built from [Recursive](https://recursive.design), with CJK glyphs from [Resource Han Rounded (资源圆体)](https://github.com/CyanoHao/Resource-Han-Rounded) and the full [Nerd Fonts](https://www.nerdfonts.com/) icon set.

| Family | Use | Spacing |
|---|---|---|
| **Rec Mono St.Helens** | Coding and terminals | Monospace, code ligatures |
| **Rec Sans Mt.Baker** | Everyday text and UI | Proportional |

Both families use the same casual, cursive design in four styles: Regular, Italic, Bold, and Bold Italic.

## Install

Download the fonts from the [latest release](https://github.com/D0n9X1n/m-fonts/releases/latest) and install them. Per-OS steps are on the [Installation](https://github.com/D0n9X1n/m-fonts/wiki/Installation) page.

## Build

```bash
brew install fontforge sevenzip
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
./scripts/build-all.sh          # → fonts/<Family>/*.ttf
```

The build downloads the upstream releases pinned in `versions.env`. See [Building](https://github.com/D0n9X1n/m-fonts/wiki/Building).

## Documentation

The [wiki](https://github.com/D0n9X1n/m-fonts/wiki) ([简体中文](https://github.com/D0n9X1n/m-fonts/wiki/Home-zh-CN)) covers the fonts, configuration, the build pipeline, and the release process. Its source is the `wiki/` directory in this repository.

## Credits

[Recursive](https://github.com/arrowtype/recursive) by Arrow Type · [Resource Han Rounded](https://github.com/CyanoHao/Resource-Han-Rounded) by CyanoHao · [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts) by Ryan L McIntyre · based on [recursive-code-config](https://github.com/arrowtype/recursive-code-config) by Arrow Type

## License

The build scripts are [MIT](LICENSE). The fonts are derived from Recursive and Resource Han Rounded, both under the [SIL Open Font License 1.1](https://openfontlicense.org), and include Nerd Fonts glyphs under their [respective licenses](https://github.com/ryanoasis/nerd-fonts/blob/master/LICENSE).
