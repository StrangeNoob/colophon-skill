---
name: colophon
description: Use when you have produced HTML, Markdown, a plan, a report, a chart, a slide deck, a single file or any directory of files and the person needs a URL for it — publishes a directory or one file to the web, renders bare Markdown as pages, updates it in place, rolls it back to an earlier version, controls who can see it — named people, or a password — and takes it down again.
license: MIT
---

# Colophon

You made the files. This gives them an address.

`colophon publish <dir|file>` packs a directory, or one file, uploads it, and prints one URL. Re-publishing the
same slug replaces what is live without changing the URL, so a link you hand someone stays
correct as the work changes.

## Installing the CLI

```bash
npm install -g @strangenoob/colophon@0.12.0
```

Or run it without installing: `npx @strangenoob/colophon@0.12.0 publish ./dir`. Needs Node 18+.
The version is pinned on purpose — it is the CLI this document describes, and the pin moves
with the skill — rather than whatever npm has on the day. An older CLI has no `make-live` and
no `password` level (0.12.0), publishes without an account when `COLOPHON_TOKEN` is set but empty (until 0.11.1),
has no `search` (0.11.0), no `versions`, `visibility`, `expire` or `--expires` (0.9.0), and
before 0.7.0 answers `colophon list` with the first fifty sites and no sign there are more;
`colophon help` shows what is installed.

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

Do not run `publish` signed out to see what happens. Since CLI 0.10.0 a signed-out publish goes
out without an account: a shared address that answers for 24 hours, with a link to claim it.
That is for someone trying Colophon, not a home for the person's work.

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

**Who should be able to open it?** Offer three — `unlisted` (anyone with the link: suggest this
one), `public` (anyone, and the only level search engines may index, if the workspace's owner
allows them), `restricted` (workspace members plus named email addresses, each asked to sign
in). Two more are there if they ask for them, or describe them: `password` (anyone with the link
who also types a password — no account, no sign-in: a client review, readers outside the
workspace) and `private` (workspace members only). Pass the answer as `--visibility` on every
publish of that site, re-publishes included — then its level is never left to whatever the CLI
defaults to. The one exception is `password`; see below.

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
- `--expires <moment>` (ISO 8601, e.g. `2026-10-01T00:00:00Z`) makes the site stop answering
  after that moment — `410` on every path, nothing deleted. For output the person only needs
  for a while, at a deadline they named; never invent one. `--expires none` clears it.

**To update a published site, publish again with the same `--slug`.** The old version is kept,
and `colophon make-live` puts it back (below); the URL does not change. Do not publish a second
site for a second draft. The summary on stderr says what the republish changed against the
version before — `+2 ~1 -1` is files added, changed, removed; `identical` means nothing moved —
so tell the person that, not just the URL.

## Rolling back, and making a draft live

```bash
colophon versions report             # v3 live, v2, v1 — each with what it changed
colophon versions report --diff 2    # what making v2 live would change against what is live now
colophon make-live report 2          # v2 is live again; the URL does not change
```

`make-live` makes one of a site's kept versions the live one. Nothing is uploaded and nothing is
deleted: the version it replaces stays, and comes back the same way. `colophon rollback` is the
same command.

- **"Undo that", "put back yesterday's version", "the last publish broke it"** — that is
  `make-live` with an earlier version, not a republish of old files. Run `versions` first, pick
  the number from it (v1 is the oldest), and name it back to the person — "v2, from 14 October,
  before the chart change" — so they can say if it is the wrong one.
- **A draft goes live the same way, once the person approves it.** A `--draft` publish prints the
  exact command, `colophon make-live <site id> <version id>`. Run it only on their word: a draft
  is there so someone looks before it goes live, and making it live because you can is the
  thing it was there to prevent.
- Tell them what moved. stdout is the URL; stderr says `v2 is live in place of v3: ~1 -1`, or
  `v2 was already live; nothing changed`.
- A version held for review cannot be made live — a Colophon admin releases or rejects it — and
  one rejected in review never can. Say so; do not retry.
- It does not touch the expiry. On an expired site the CLI says so — the site still answers
  `410`, and bringing it back (`colophon expire <slug> none`) is the owner's call.

## Choosing visibility

The second question in full. `unlisted` is the one that matches what people usually mean by
"send me a link", so suggest it when they have no view.

| | Who can open it |
|---|---|
| `public` | Anyone. Search engines may index it once the workspace's owner allows them — off by default. |
| `unlisted` | Anyone with the link. Never indexed. **Default.** |
| `password` | Anyone with the link who types the password. No sign-in; members are asked too. Never indexed. |
| `restricted` | Workspace members, plus named email addresses. Each is asked to sign in. |
| `private` | Workspace members only. |

`restricted` and `private` mean the reader signs in first, so do not use them for a link
someone needs to open on their phone in a hurry unless access control actually matters.

To add a named reader to a `restricted` site, open the site in the dashboard and add the
address under **Shared with** — the person does not need an account first.

### A password

The password is the person's to choose. Ask for it; never make one up unasked, and if they ask
you to pick, tell them what you picked. It is never an argument (`--password` is refused, since it
would sit in shell history and `ps`), and it never goes in the site's files.

The best way keeps it out of this chat and off every command line: give the person the command
to run in their own terminal, where the CLI asks for it twice and echoes nothing.

```bash
colophon publish ./review --slug review --visibility password
```

When they would rather tell you, pipe it in from your own shell. The CLI asks in a terminal only,
so a command you run must bring the password with it:

```bash
printf '%s' 'the password' | colophon publish ./review --slug review --visibility password --password-stdin
```

- That line carries the password, so it is for running yourself, never for handing to a person:
  an interactive shell saves every line in its history. Anything they run themselves is the
  prompting form above.
- In a script, take it from a variable the person set — `printf '%s' "$SITE_PASSWORD" | …` —
  never a literal.
- At least six characters, and no space at either end. If the server refuses one, ask for
  another; do not trim or pad theirs yourself.
- **Re-publishing a password site: leave both `--visibility` and `--password-stdin` off.** The
  level and the password stay as they are, and nothing asks for one. Sending the password again,
  even the same one, counts as a new one: every reader would have to type it again.
- The CLI answers `password set — give it to your readers yourself`: Colophon keeps only a hash
  and can never show it again. Tell the person to keep it with the link and send it to readers
  their own way. Lost, it is replaced, not recovered.
- To change it, the person runs `colophon visibility <slug> password` in their own terminal and
  types the new one at the prompt; if they tell you instead, pipe it with `--password-stdin`, as
  above. Everyone holding the old one is asked again. That, and moving the site to another level
  (which discards the password), is an owner's decision, like any change of level.
- A reader types it at the page and stays in for an hour in that browser, then types it again.
  Nobody signs in, so a password page has no comments and no list of who opened it. If the
  person wants either, that is `restricted`.

## Publishing from CI

When the person wants a site published from CI — docs on every push to main, a report a scheduled
job rebuilds — it is one step: this CLI through `npx`, pinned, with the key from a secret. In
GitHub Actions:

```yaml
- id: site
  run: |
    url=$(npx -y @strangenoob/colophon@0.12.0 publish ./dist --slug docs --visibility unlisted)
    echo "url=$(tail -n 1 <<< "$url")" >> "$GITHUB_OUTPUT"
  env:
    COLOPHON_TOKEN: ${{ secrets.COLOPHON_TOKEN }}
- run: echo "Published to ${{ steps.site.outputs.url }}"
```

- **Pin the version** as above, so a CLI release never changes the workflow under the person.
  Move it with this skill.
- **Always set `--slug`.** The workflow runs again and again, and a fixed slug is what makes every
  run update the same URL instead of adding a site — each new slug counts against the plan.
- **The key is the person's to set.** Ask them to mint one (`colophon create-token --name ci` on
  their own machine, or **API keys** in the dashboard) and add it as the repository secret
  `COLOPHON_TOKEN` under **Settings → Secrets and variables → Actions**. Never write a key into
  the workflow, and never ask for it in chat. The key's workspace is where the site lands, so the
  workspace question is already answered; still ask who should be able to open it.
- `url=$(…)` on a line of its own is what makes a failed publish fail the step; the second line
  keeps the URL, the last line the CLI prints, for a PR comment or a deployment.
- `COLOPHON_TOKEN is set but empty` means the secret is missing, misnamed, or withheld — a pull
  request from a fork gets no secrets. The CLI refuses rather than publishing without an account.
  Publish on `push`, or on pull requests from branches of the same repository.
- `COLOPHON_API` in the step's `env` points it at a self-hosted instance.
- A `password` site from CI: publish it the first time from a terminal with its password (see
  [A password](#a-password)), and leave `--visibility` off in the workflow. Every run then keeps
  the level and the password; piping it in on each run would make every reader type it again.

There is no Colophon GitHub Action to `uses:`; this step is the supported way. Details at
https://colophon.fyi/docs/cli#ci.

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
colophon search <words>              # which live page says it, across every site in the workspace
colophon versions <slug>             # every version, newest first, with what each one changed
colophon versions <slug> --diff 2    # what making v2 live would change against what is live now
colophon make-live <slug> 2          # make v2 the live version: a rollback, or a draft approved
colophon visibility <slug> <level>   # change who can open a site without republishing it
colophon expire <slug> <moment>      # when it stops answering: 410 on every path, nothing deleted
colophon expire <slug> none          # clear that, so it answers again
colophon delete <slug>               # permanently removes a site and every version
colophon link <url> --code q3        # a short redirect on the workspace's own domain
colophon switch [workspace]          # list the workspaces the person belongs to, or work in another
colophon skill install [agent ...]   # put this skill in front of the person's other coding agents
```

`versions` answers "what changed?" without opening two pages: `+2 ~1 -1` per version, or
`identical` for a republish that moved nothing, and `--diff <n> --patch <path>` prints one
file's unified diff. `--diff <n>` is the check to run before `make-live <n>`.

`search` answers "which report mentioned X": the text of every site live in the workspace,
restricted and private included, best match first, each with its URL and the passage that
matched. `"a phrase"` goes in quotes, quoted again for the shell, and `-word` leaves one out.

`visibility` and `expire` change a site in place, on the person's word only — they are the
person's decisions, like the two questions above. Name the level or the moment back to them.
To `password`, pipe the password in with `--password-stdin`, as above.
`expire` with a moment already past takes the site down now and deletes nothing; `none`, or a
later moment, brings it back.

`delete` is not reversible and does not ask. Only run it when the person asked for that site
to come down, and name the slug back to them when you do.

## When it fails

- `not signed in` — ask the person to run `colophon login` (or, headless, for a key), as above.
- `your session has expired` — the login lapsed or was revoked. Ask them to run `colophon login` again.
- `invalid or revoked key` — the key in `COLOPHON_TOKEN` was revoked or copied wrong. Ask for a fresh one.
- `this command needs a signed-in session` — you ran `create-token` or `switch` with a key. Those are for the person's own terminal.
- `publishing live needs the publisher role or above; yours in this workspace is editor` — on
  `publish` or `make-live`: the person's role lets them publish drafts only. Publish with
  `--draft` and give them the preview URL and the `make-live` command it printed; a publisher or
  owner runs that, or uses **Make live** in the dashboard. Do not ask them to change roles.
- `… needs the owner role or above` on `visibility`, `expire` or `delete`, or `changing an
  existing site's visibility is for owners` (or `password is for owners`) on a republish — those
  are an owner's decisions. Republish without `--visibility` or `--password-stdin` to keep the
  site as it is, and say who can change it.
- `visibility 'password' needs a password for readers to type` — the level went without one.
  Ask the person for it and pipe it in with `--password-stdin`.
- `password must be at least 6 characters`, `… cannot start or end with a space` — ask for
  another. `--password-stdin read nothing` — the pipe was empty. `--password would leave it in
  your shell history` — pipe it instead.
- `quota exceeded: sites (4 > 3)` — the plan's site limit. Either `colophon delete` a site
  that is finished with, or the person upgrades. Do not delete one to make room on your own.
- `archive contains no files` — the directory is empty, or everything in it was skipped.
- `held for review` — the upload was stored but is not live yet. Say so; do not retry.
- `… is held for review and cannot be made live` or `… was rejected in review` on `make-live` —
  that version cannot be put live this way. Say so, and offer an earlier version instead.
- `no version 9 of <slug>` — the number is not one `colophon versions <slug>` prints. Run it and
  pick again.

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
