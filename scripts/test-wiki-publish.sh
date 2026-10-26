#!/usr/bin/env bash
# test-wiki-publish.sh — Exercise publish-wiki.sh against a throwaway wiki repo
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
publisher="$root/scripts/publish-wiki.sh"

fail() {
  printf 'wiki publish test: %s\n' "$1" >&2
  exit 1
}

[[ -x "$publisher" ]] || fail "publisher is missing or not executable"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
source_dir="$tmp/source"
wiki_repo="$tmp/wiki"
mkdir -p "$source_dir"
git init -q -b master "$wiki_repo"
git -C "$wiki_repo" config user.name test
git -C "$wiki_repo" config user.email test@example.invalid
printf '# stale\n' > "$wiki_repo/Stale.md"
printf '# old\n' > "$wiki_repo/Keep.md"
git -C "$wiki_repo" add --all
git -C "$wiki_repo" commit -q -m seed

printf '# home\n' > "$source_dir/Home.md"
printf '# 首页\n' > "$source_dir/Home-zh-CN.md"
printf '# current\n' > "$source_dir/Keep.md"
printf 'not a wiki page\n' > "$source_dir/ignored.txt"

# First publish: adds, updates, and deletes pages in one commit
out="$tmp/first-output"
GITHUB_OUTPUT="$out" "$publisher" "$source_dir" "$wiki_repo" 0123456789abcdef > /dev/null
[[ "$(<"$out")" == "changed=true" ]] || fail "changed publish did not request a push"
[[ -f "$wiki_repo/Home.md" && -f "$wiki_repo/Home-zh-CN.md" ]] || fail "publisher omitted a new page"
[[ "$(<"$wiki_repo/Keep.md")" == "# current" ]] || fail "publisher did not update a page"
[[ ! -e "$wiki_repo/Stale.md" ]] || fail "publisher kept a deleted page"
[[ ! -e "$wiki_repo/ignored.txt" ]] || fail "publisher copied a non-Markdown file"
[[ "$(git -C "$wiki_repo" rev-list --count HEAD)" == "2" ]] || fail "first publish did not create one commit"
[[ "$(git -C "$wiki_repo" log -1 --pretty=%s)" == "Publish wiki from 0123456" ]] || fail "commit does not name the source SHA"

# Second publish of the same source: no commit, no push
out="$tmp/second-output"
GITHUB_OUTPUT="$out" "$publisher" "$source_dir" "$wiki_repo" fedcba9876543210 > /dev/null
[[ "$(<"$out")" == "changed=false" ]] || fail "unchanged publish requested a push"
[[ "$(git -C "$wiki_repo" rev-list --count HEAD)" == "2" ]] || fail "unchanged publish created a commit"

# Refuses a destination that is not on master
git -C "$wiki_repo" switch -q -c other
if "$publisher" "$source_dir" "$wiki_repo" 0123456 > /dev/null 2>&1; then
  fail "publisher accepted a non-master destination"
fi

printf 'wiki publish test: ok\n'
