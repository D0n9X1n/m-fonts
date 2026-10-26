# 安装

[English](Installation)

从[最新发布](https://github.com/D0n9X1n/m-fonts/releases/latest)下载字体。每个发布包含
八个 `.ttf` 文件、含全部八个文件的 `m-fonts-<tag>.zip`，以及 `SHA256SUMS.txt`。

## 安装字体

| 系统 | 步骤 |
|---|---|
| macOS | 把 `.ttf` 文件复制到 `~/Library/Fonts/` |
| Linux | 复制到 `~/.local/share/fonts/`，然后运行 `fc-cache -f` |
| Windows | 选中文件，右键，选择**安装** |

校验下载的文件：

```bash
shasum -a 256 --check SHA256SUMS.txt   # Linux：sha256sum --check SHA256SUMS.txt
```

## 在应用中使用

按名称选择字体。会缓存字体列表的应用需要重启。

| 用途 | 字体名称 |
|---|---|
| 终端、编辑器 | `Rec Mono St.Helens` |
| 文档、界面 | `Rec Sans Mt.Baker` |

## 从旧版本升级

m-fonts v2.0.0 之前的版本发布在 `MOSconfig/recursive-code-config`，其中的
**Rec Mono Baker** 是等宽的直线风格字体，现由 Mt.Baker 取代。安装 v2.0.0 之前：

1. 从字体文件夹删除 `RecMonoBaker-*.ttf`。
2. 替换四个 `RecMonoSt.Helens-*.ttf` 文件。
3. 在原来使用 `Rec Mono Baker` 的应用里改选 `Rec Sans Mt.Baker`。

每套字体只保留一份。同名的两份字体会让系统随机选用其中一份。
