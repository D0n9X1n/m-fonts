# m-fonts

[![Release](https://img.shields.io/github/v/release/D0n9X1n/m-fonts?sort=semver)](https://github.com/D0n9X1n/m-fonts/releases/latest)
[![CI](https://img.shields.io/github/actions/workflow/status/D0n9X1n/m-fonts/ci.yml?branch=main&label=CI)](https://github.com/D0n9X1n/m-fonts/actions/workflows/ci.yml)
[![Font license: OFL-1.1](https://img.shields.io/badge/Font_license-OFL_1.1-lightgreen.svg)](https://openfontlicense.org)

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
