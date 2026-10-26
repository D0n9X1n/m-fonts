# 配置

[English](Configuration)

每套字体对应 `configs/` 中的一个 YAML 文件。上游版本记录在 `versions.env`。

## 字体配置

`configs/st-helens.yaml` 保存共同的设计：

| 键 | 含义 |
|---|---|
| `Family Name` | 完整字体名，例如 `Rec Mono St.Helens`。文件名和 PostScript 名去掉空格。 |
| `Mono` | `true` 构建等宽字体（`MONO 1`）；`false` 构建比例字体（`MONO 0`） |
| `Styles` | Regular、Italic、Bold、Bold Italic 各自的 `CASL`、`wght`、`slnt` 和 `CRSV` |
| `Code Ligatures` | 默认开启 Recursive 的代码连字。只对等宽字体生效。 |
| `Features` | 固化进字体的风格集 |

`configs/mt-baker.yaml` 以 St.Helens 为基础：

```yaml
Extends: st-helens.yaml

Family Name: Rec Sans Mt.Baker
Mono: false
```

`Extends` 先加载指定文件，再用当前文件中的键覆盖父配置。因此对 St.Helens 样式或
风格集的修改也会作用到 Mt.Baker。

## 代码连字

Recursive 把代码连字画成宽于一格的字形。对等宽字体，构建会把每个连字的步进宽度设为
一格，并把轮廓左移，覆盖到前面的单元格上。在比例字体中这会压缩所有宽于空格的字形，
因此当 `Mono` 为 `false` 时，即使 `Code Ligatures` 为 `true`，构建也会跳过连字。

## 风格集

| 特性 | 变化 | 适用 |
|---|---|---|
| ss01 | 单层 a | 仅正体 |
| ss02 | 单层 g | 仅正体 |
| ss03 | 简化 f | 仅正体 |
| ss04 | 简化 i | 仅正体 |
| ss05 | 简化 l | 仅正体 |
| ss06 | 简化 r | 仅正体 |
| ss07 | 简化斜体斜笔画（kwxyz） | 正体和手写体 |
| ss08 | 无衬线 L 和 Z | 正体和手写体 |
| ss09 | 简化 6 和 9 | 正体和手写体 |
| ss10 | 带点的 0 | 正体和手写体 |
| ss11 | 简化 1 | 正体和手写体 |
| ss12 | 简化 @ | 正体和手写体 |

## 上游版本

`versions.env` 固定每个上游发布：

```bash
RECURSIVE_VERSION=1.085
RESOURCE_HAN_ROUNDED_VERSION=0.990
NERD_FONTS_VERSION=3.5.1
```

`./scripts/check-updates.sh` 把这些版本与 GitHub 上的最新发布（不含预发布）比较，
有落后时以状态码 1 退出。要更新某个版本，修改版本号，运行
`./scripts/local-gate.sh --build`，并在编辑器中检查效果后再合并。

## 添加字体

1. 新建 `configs/<名称>.yaml`，通常写上 `Extends: st-helens.yaml`。
2. 运行 `./scripts/build.sh configs/<名称>.yaml`。

`build-all.sh`、校验脚本、CI 和发布打包都会自动处理 `configs/` 中的每个文件。
