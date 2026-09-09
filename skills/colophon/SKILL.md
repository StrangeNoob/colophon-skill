---
name: colophon
description: Use when you have produced HTML, Markdown, a plan, a report, a chart, a slide deck, a single file or any directory of files and the person needs a URL for it — publishes a directory or one file to the web, renders bare Markdown as pages, updates it in place, controls who can see it, and takes it down again.
license: MIT
---

# Colophon

You made the files. This gives them an address.

`colophon publish <dir|file>` packs a directory, or one file, uploads it, and prints one URL. Re-publishing the
same slug replaces what is live without changing the URL, so a link you hand someone stays
correct as the work changes.

## Installing the CLI

```bash
npm install -g @strangenoob/colophon
```

Or run it without installing: `npx @strangenoob/colophon publish ./dir`. Needs Node 18+ and
version 0.6.0 or later — everything below assumes it.

## Before the first publish

Run `colophon whoami`. It prints who is signed in and which workspace publishes will land in.
If it says `not signed in`, stop and ask — you cannot sign in on the person's behalf, because
both ways need them:

- **On their own machine** (the usual case): ask them to run `colophon login` in a terminal.
  It opens their browser; they click Approve once, and the session lasts 30 days from its
  last use. Nothing is pasted and nothing goes in a shell profile.

  > I need to be signed in to publish. Please run `colophon login` in a terminal and approve
  > it in the browser, then tell me.

- **Headless — CI, a server, a sandbox with no browser:** ask for an API key set as
  `COLOPHON_TOKEN` in this environment. They can mint one from their own machine with
  `colophon create-token --name <agent-name>`, or under **API keys** in the dashboard. It is
  shown once.

Never ask for a key when `login` would do; a key in a chat transcript is a key to revoke.

If they ask what `login` does, where the session lives, or how to revoke it, point them at
https://colophon.fyi/docs/signin rather than explaining from memory.

## Ask two things first

Where the site lives and who can open it are the person's to decide, and `whoami`'s answer is
only a default. Ask both in one message, once per conversation — not before every publish — and
skip whichever they have already answered ("put it on the team workspace, anyone with the link"
is both).

**Which workspace?** `colophon switch` with no argument lists every workspace they belong to,
with `*` on the one publishes land in now:

```bash
colophon switch          # * acme   owner    Acme Inc
                         #   side   member   Side Projects
colophon switch side     # publish into that one from now on
```

One line means one workspace: name it and move on. Signed in with `COLOPHON_TOKEN` there is
nothing to ask either — a key belongs to one workspace, `whoami` names it, and `switch` refuses.
Pass the left-hand column to `switch`; the display name is not what it matches on.

**Who should be able to open it?** Offer three — `unlisted` (anyone with the link, not indexed:
suggest this one), `public` (anyone, indexed by search engines), `restricted` (workspace members
plus named email addresses, each asked to sign in). `private`, workspace members only, is there
if they ask for it. Pass the answer as `--visibility` on every publish of that site, re-publishes
included — then its level is never left to whatever the CLI defaults to.

## Publishing

```bash
colophon publish ./report --name "Q3 report" --visibility unlisted
colophon publish plan.md                         # one file is a site of one page
```

Prints the URL on stdout and a one-line summary on stderr. Give the person the URL.

- Publish what you made as it is. A plan, a spec or a report in Markdown needs no HTML
  wrapping: every `.md` is rendered to an `.html` beside it at publish time, with links between
  Markdown files rewritten to match. A `README.md` or `index.md` stands in for a missing
  `index.html`, and a root with neither shows the one page it has, or a listing of every file.
  The original files stay at their own URLs. To keep a Markdown file unrendered, ship your own
  `x.html` beside `x.md`.
- `--name` is the display name in the dashboard. Defaults to the directory name.
- `--slug` fixes the URL path. Defaults to a slug derived from the name — pass it explicitly
  when you intend to update this site later, so a changed name cannot move the URL.
- `.git`, `.env`, `node_modules` and editor junk are never uploaded.

**To update a published site, publish again with the same `--slug`.** The old version is kept
and can be rolled back from the dashboard; the URL does not change. Do not publish a second
site for a second draft.

## Choosing visibility

The second question in full. `unlisted` is the one that matches what people usually mean by
"send me a link", so suggest it when they have no view.

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

## Their own domain

A workspace can answer on a hostname of its own — `https://m.example.dev/report/` instead of
`https://acme.usercontent.colophon.fyi/report/`. Once it is live, that is the URL `publish` and
`list` print; the subdomain form keeps working too. Hand the person whichever the CLI printed —
both are correct.

Attaching one is an owner's job in the dashboard (**Members → Workspace**), not something you
can do from the CLI. If the person asks for their sites on their own domain, tell them where,
and what to expect: they type the hostname, get two DNS records to add (a TXT that proves it is
theirs and a CNAME to their subdomain), and their URLs switch on their own once both resolve —
nothing needs republishing. Details at https://colophon.fyi/docs/workspaces#domain.

## Other commands

```bash
colophon list                        # slug, visibility and URL for every site
colophon delete <slug>               # permanently removes a site and every version
colophon link <url> --code q3        # a short redirect on the workspace's own domain
colophon switch [workspace]          # list the workspaces the person belongs to, or work in another
colophon skill install [agent ...]   # put this skill in front of the person's other coding agents
```

`delete` is not reversible and does not ask. Only run it when the person asked for that site
to come down, and name the slug back to them when you do.

## When it fails

- `not signed in` — ask the person to run `colophon login` (or, headless, for a key), as above.
- `your session has expired` — the login lapsed or was revoked. Ask them to run `colophon login` again.
- `invalid or revoked key` — the key in `COLOPHON_TOKEN` was revoked or copied wrong. Ask for a fresh one.
- `this command needs a signed-in session` — you ran `create-token` or `switch` with a key. Those are for the person's own terminal.
- `quota exceeded: sites (4 > 3)` — the plan's site limit. Either `colophon delete` a site
  that is finished with, or the person upgrades. Do not delete one to make room on your own.
- `archive contains no files` — the directory is empty, or everything in it was skipped.
- `held for review` — the upload was stored but is not live yet. Say so; do not retry.

## Notes

- Docs live at https://colophon.fyi/docs — the sign-in flow is /docs/signin, the CLI reference
  /docs/cli, access levels /docs/access. Link to them instead of paraphrasing when the person
  wants detail.
- If the person asks how to get this skill into Codex, Cursor, Gemini CLI, Copilot, OpenCode or
  another agent: `colophon skill install` detects what is on the machine and installs
  into each; `colophon skill install codex` picks one. Details at https://colophon.fyi/docs/skill.

- Every published page carries a small analytics beacon. Views, referrers and devices show up
  under the site in the dashboard. No cookies are set and no visitor is identified.
- `COLOPHON_API` overrides the API origin for a self-hosted instance.
