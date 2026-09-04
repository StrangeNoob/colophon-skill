---
name: colophon
description: Use when you have produced HTML, a report, a chart, a slide deck or any directory of files and the person needs a URL for it — publishes a directory to the web, updates it in place, controls who can see it, and takes it down again.
---

# Colophon

You made the files. This gives them an address.

`colophon publish <dir>` packs a directory, uploads it, and prints one URL. Re-publishing the
same slug replaces what is live without changing the URL, so a link you hand someone stays
correct as the work changes.

## Installing the CLI

```bash
npm install -g @strangenoob/colophon
```

Or run it without installing: `npx @strangenoob/colophon publish ./dir`. Needs Node 18+.

## Before the first publish

Publishing needs a key, and only a person can create one. If `COLOPHON_TOKEN` is unset, stop
and ask for it rather than guessing:

> Publishing needs an API key. Sign in at https://app.colophon.fyi, open **Keys**, create one,
> and set `COLOPHON_TOKEN` to the value it shows you — it is shown once.

Check with `colophon whoami`, which prints the workspace the key belongs to.

## Publishing

```bash
colophon publish ./report --name "Q3 report" --visibility unlisted
```

Prints the URL on stdout and a one-line summary on stderr. Give the person the URL.

- `<dir>` needs an `index.html` at its top level to have a working root. The CLI warns if not.
- `--name` is the display name in the dashboard. Defaults to the directory name.
- `--slug` fixes the URL path. Defaults to a slug derived from the name — pass it explicitly
  when you intend to update this site later, so a changed name cannot move the URL.
- `.git`, `.env`, `node_modules` and editor junk are never uploaded.

**To update a published site, publish again with the same `--slug`.** The old version is kept
and can be rolled back from the dashboard; the URL does not change. Do not publish a second
site for a second draft.

## Choosing visibility

Default to `unlisted` unless the person says otherwise. It is the one that matches what people
usually mean by "send me a link".

| | Who can open it |
|---|---|
| `public` | Anyone. Indexed by search engines. |
| `unlisted` | Anyone with the link. Not indexed. **Default.** |
| `restricted` | Workspace members, plus named email addresses. Each is asked to sign in. |
| `private` | Workspace members only. |

`restricted` and `private` mean the reader signs in first, so do not use them for a link
someone needs to open on their phone in a hurry unless access control actually matters.

To add a named reader to a `restricted` site, open the site in the dashboard and add the
address under **Shared with** — the person does not need an account first.

## Other commands

```bash
colophon list                        # slug, visibility and URL for every site
colophon delete <slug>               # permanently removes a site and every version
colophon link <url> --code q3        # a short redirect on the workspace's own domain
```

`delete` is not reversible and does not ask. Only run it when the person asked for that site
to come down, and name the slug back to them when you do.

## When it fails

- `COLOPHON_TOKEN is not set` — ask for a key, as above.
- `invalid or revoked key` — the key was revoked or copied wrong. Ask for a fresh one.
- `quota exceeded: sites (4 > 3)` — the plan's site limit. Either `colophon delete` a site
  that is finished with, or the person upgrades. Do not delete one to make room on your own.
- `archive contains no files` — the directory is empty, or everything in it was skipped.
- `held for review` — the upload was stored but is not live yet. Say so; do not retry.

## Notes

- Every published page carries a small analytics beacon. Views, referrers and devices show up
  under the site in the dashboard. No cookies are set and no visitor is identified.
- `COLOPHON_API` overrides the API origin for a self-hosted instance.
