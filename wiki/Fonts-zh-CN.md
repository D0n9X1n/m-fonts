# 字体

[English](Fonts)

m-fonts 提供两套共用同一设计的字体。St.Helens 用于写代码；Mt.Baker 是相同的字形，
但使用自然字宽，用于日常文本。

## 字体家族

| 字体 | 用途 | 字宽 | 代码连字 |
|---|---|---|---|
| **Rec Mono St.Helens** | 编辑器和终端 | 等宽，单元格 600 单位 | 有 |
| **Rec Sans Mt.Baker** | 文档和界面 | 比例宽度 | 无 |

每套字体有四种样式：Regular、Italic、Bold 和 Bold Italic。

## 共同设计

两套字体来自同一份配置（`configs/st-helens.yaml`）；Mt.Baker 只改了名称和字宽。
见[配置](Configuration-zh-CN)。

| 设置 | 值 |
|---|---|
| 休闲度（`CASL`） | 1 — Recursive 的休闲笔刷风格 |
| 手写体（`CRSV`） | 1 — 手写体字形 |
| 倾斜（`slnt`） | Regular 和 Bold 为 -4°，Italic 和 Bold Italic 为 -10° |
| 字重（`wght`） | Regular 和 Italic 为 400，Bold 和 Bold Italic 为 600 |
| 风格集 | ss01–ss12，包括带点的零（ss10） |

Recursive 的 ss01–ss06 只作用于正体（`CRSV 0`）字形，因此在 `CRSV 1` 下看不出变化。
它们保留在配置里，方便正体字体复用。

## 字形覆盖

| 来源 | 覆盖范围 |
|---|---|
| Recursive | 拉丁、希腊、西里尔字母、标点和符号 |
| 资源圆体 CN | 汉字（U+4E00–9FFF 中 20,976 个）、假名、CJK 标点、全角和半角字符 |
| Nerd Fonts | 补丁工具 `--complete` 选项加入的全部图标集，包括 Powerline |

Regular 和 Italic 使用资源圆体 Regular 字重的中日文字形，Bold 和 Bold Italic
使用其 Bold 字重。字形按 Recursive 的行高缩放 1.15 倍。不包含韩文音节。

## 字宽差异

| 字形组 | St.Helens | Mt.Baker |
|---|---|---|
| ASCII | 固定 600 | 自然宽度（例如 `i` 350、`m` 850） |
| 汉字和全角字符 | 1200（两格） | 按比例缩放的原始宽度（1150） |
| 半角字符 | 600（一格） | 按比例缩放的原始宽度（575） |
| Nerd Font 图标 | 两格，居中 | 自然宽度 |
| 代码连字（`=>`、`!=`） | 默认开启 | 关闭 |

St.Helens 还设置了 Windows Terminal 和 DirectWrite 让 ASCII 保持在单元格网格上所需的标志；
见[构建流程](Build-Pipeline-zh-CN)。
