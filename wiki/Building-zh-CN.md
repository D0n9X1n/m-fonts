# 构建

[English](Building)

构建过程把固定版本的上游发布转换成八个发布字体，在本地和 CI 中的运行方式相同。

## 前置依赖

| 工具 | macOS | Debian/Ubuntu |
|---|---|---|
| Python 3 | Xcode 工具或 Homebrew 自带 | `python3`、`python3-venv` |
| FontForge | `brew install fontforge` | `apt-get install fontforge python3-fontforge` |
| 7-Zip | `brew install sevenzip` | `apt-get install p7zip-full` |
| curl、unzip | 系统自带 | 系统自带 |

Python 包的版本固定在 `requirements.txt`：

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## 构建字体

```bash
./scripts/build-all.sh                       # 并行构建 configs/ 中的所有字体
./scripts/build.sh configs/st-helens.yaml    # 只构建一套
./scripts/build-all.sh 1.2                   # 覆盖中日文缩放比例（默认 1.15）
```

输出位于 `fonts/<紧凑字体名>/`，例如
`fonts/RecMonoSt.Helens/RecMonoSt.Helens-Regular.ttf`。在 Apple Silicon Mac 上
完整构建约需 90 秒。

## 上游源文件

首次构建会运行 `scripts/fetch-sources.sh`，把 `versions.env` 中固定的版本下载到 `sources/`：

| 目录 | 内容 |
|---|---|
| `sources/recursive/` | `Recursive_VF_<版本>.ttf` 和代码连字特性文件 |
| `sources/resource-han-rounded/` | `ResourceHanRoundedCN-Regular.ttf` 和 `-Bold.ttf` |
| `sources/nerd-fonts-patcher/` | Nerd Fonts 的 `font-patcher` 及其图标源文件 |

每个目录在 `.version` 中记录版本；在 `versions.env` 改变之前，后续构建会跳过下载。
`sources/`、`build/` 和 `fonts/` 均被 git 忽略。

## 检查

```bash
./scripts/local-gate.sh            # 脚本、配置、百科、发布说明（几秒）
./scripts/local-gate.sh --build    # 同时构建并校验所有字体
```

提交拉取请求前先运行检查。CI 运行相同的检查；见[发布流程](Release-Process-zh-CN)。
