# Wiki Publication

[简体中文](Wiki-Publication-zh-CN)

The tracked `wiki/` directory is the only documentation source. Each topic has an
English `<Page>.md` and a Chinese `<Page>-zh-CN.md` with the same heading
structure and equivalent facts. Update both files in the same change, and check
descriptions against the current scripts and configs.

## Rules

- Pages link by bare page name — `[Building](Building)`, not `Building.md`.
- Links stay in the page's language, except the language-switch link at the top.
- `Home` links to every English page; `Home-zh-CN` links to every Chinese page.
- Pages sit directly in `wiki/`; subdirectories are not published.
- Use Mermaid for flows, with the same structure and localized labels.

`scripts/check-wiki.py` enforces these rules and runs in the local gate:

```bash
python3 scripts/check-wiki.py
```

It checks page destinations, not heading anchors; check anchor links in the
rendered pages.

## Publication

After every push to `main`, `.github/workflows/publish-wiki.yml` clones the
GitHub wiki repository, replaces its Markdown pages with `wiki/*.md` using
`scripts/publish-wiki.sh`, and pushes only when something changed. The commit
message names the source commit. Edits made directly in the GitHub wiki are
overwritten by the next publication, so change the files in `wiki/` instead.

`scripts/test-wiki-publish.sh` tests the publisher against a throwaway
repository: added, updated, and deleted pages, the no-change case, and refusal
of a destination that is not on `master`.
