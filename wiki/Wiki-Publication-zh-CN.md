# 百科发布

[English](Wiki-Publication)

受版本控制的 `wiki/` 目录是唯一的文档来源。每个主题有英文 `<Page>.md` 和中文
`<Page>-zh-CN.md`，两者标题结构相同、内容等价。在同一次修改中更新两个文件，并对照当前的
脚本和配置核实描述。

## 规则

- 页面用裸页面名链接 — `[构建](Building-zh-CN)`，而不是 `Building.md`。
- 除顶部的语言切换链接外，链接保持在本页面的语言内。
- `Home` 链接到每个英文页面；`Home-zh-CN` 链接到每个中文页面。
- 页面直接放在 `wiki/` 下；子目录不会发布。
- 流程图使用 Mermaid，结构相同、标签本地化。

`scripts/check-wiki.py` 检查这些规则，并在本地检查中运行：

```bash
python3 scripts/check-wiki.py
```

它检查页面目标，不检查标题锚点；锚点链接请在渲染后的页面中检查。

## 发布

每次推送到 `main` 后，`.github/workflows/publish-wiki.yml` 克隆 GitHub 百科仓库，
用 `scripts/publish-wiki.sh` 以 `wiki/*.md` 替换其中的 Markdown 页面，只在有变化时推送。
提交信息包含源提交。直接在 GitHub 百科中的编辑会被下一次发布覆盖，请改 `wiki/` 中的文件。

`scripts/test-wiki-publish.sh` 在临时仓库中测试发布脚本：新增、更新和删除页面，
无变化的情况，以及拒绝不在 `master` 分支上的目标。
