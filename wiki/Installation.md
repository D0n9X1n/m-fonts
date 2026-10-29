# Installation

[简体中文](Installation-zh-CN)

Download the fonts from the
[latest release](https://github.com/D0n9X1n/rec-mountain-fonts/releases/latest). Each
release has the twelve `.ttf` files, `rec-mountain-fonts-<tag>.zip` with all twelve, and
`SHA256SUMS.txt`.

## Install

| OS | Steps |
|---|---|
| macOS | Copy the `.ttf` files to `~/Library/Fonts/` |
| Linux | Copy them to `~/.local/share/fonts/`, then run `fc-cache -f` |
| Windows | Select the files, right-click, and choose **Install** |

To check a download:

```bash
shasum -a 256 --check SHA256SUMS.txt   # Linux: sha256sum --check SHA256SUMS.txt
```

## Use in apps

Select the family by name. Apps that cache their font list need a restart.

| Use | Family name |
|---|---|
| Terminal, editor | `Rec Mono St.Helens` |
| Documents, UI | `Rec Sans Mt.Baker` |
| Long-form reading | `Rec Serif Mt.Adams` |

## Upgrade from older releases

Releases before v2.0.0 came from `MOSconfig/recursive-code-config`, which
has since been deleted, and shipped **Rec Mono Baker**, a monospace linear
family. Mt.Baker replaces it.
Before installing v2.0.0:

1. Delete `RecMonoBaker-*.ttf` from your fonts folder.
2. Replace the four `RecMonoSt.Helens-*.ttf` files.
3. In apps that used `Rec Mono Baker`, select `Rec Sans Mt.Baker`.

Keep only one copy of each family installed. Two copies with the same name make
the OS pick one unpredictably.
