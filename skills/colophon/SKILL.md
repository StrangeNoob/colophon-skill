---
name: colophon
description: Use when you have produced HTML, Markdown, a plan, a report, a chart, a slide deck, a single file or any directory of files and the person needs a URL for it — publishes a directory or one file to the web, renders bare Markdown as pages, serves a built single-page app, updates it in place, sends a version for a person's approval, rolls it back to an earlier version, controls who can see it — named people, or a password — says who opened it and how far they read, and takes it down again.
license: MIT
---

# Colophon

You made the files. This gives them an address.

`colophon publish <dir|file>` packs a directory, or one file, uploads it, and prints one URL. Re-publishing the
same slug replaces what is live without changing the URL, so a link you hand someone stays
correct as the work changes.

## Installing the CLI

```bash
npm install -g @strangenoob/colophon@0.15.0
```

Or run it without installing: `npx @strangenoob/colophon@0.15.0 publish ./dir`. Needs Node 18+.
The version is pinned on purpose — it is the CLI this document describes, and the pin moves
with the skill — rather than whatever npm has on the day. An older CLI has no `spa` or `--spa`
(0.15.0); has no `review` or `--review` (0.14.0), and before that calls a version the workspace's
approval rule sent for review a draft to `make-live`; holds the whole archive in memory while it
uploads (until 0.13.0); has no `make-live` and no `password` level (0.12.0); publishes without an
account when `COLOPHON_TOKEN` is set but empty (until 0.11.1); has no `search` (0.11.0), no
`versions`, `visibility`, `expire` or `--expires` (0.9.0); and before 0.7.0 answers
`colophon list` with the first fifty sites and no sign there are more. `colophon help` shows what
is installed.

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
- **A `.zip` you were handed: unzip it and publish the directory.** The CLI packs whatever path
  it is given, so `colophon publish site.zip` puts up the zip itself, one file to download. The
  dashboard takes a `.zip` as it is — dropped on the **Sites** page, like a folder — and so does
  `POST /api/v1/sites` beside a `.tar.gz`; a `.zip` whose files share one top folder publishes
  that folder.
- `--expires <moment>` (ISO 8601, e.g. `2026-10-01T00:00:00Z`) makes the site stop answering
  after that moment — `410` on every path, nothing deleted. For output the person only needs
  for a while, at a deadline they named; never invent one. `--expires none` clears it.
- A built React, Vite or Vue app needs `--spa` and the right base path; see
  [A built app, and redirects](#a-built-app-and-redirects). Work someone else must agree to first
  goes out with `--review`; see [Sending it for review](#sending-it-for-review).

**To update a published site, publish again with the same `--slug`.** The old version is kept,
and `colophon make-live` puts it back (below); the URL does not change. Do not publish a second
site for a second draft. The summary on stderr says what the republish changed against the
version before — `+2 ~1 -1` is files added, changed, removed; `identical` means nothing moved —
so tell the person that, not just the URL.

## A built app, and redirects

```bash
vite build --base=/app/                          # the address the site will have
colophon publish ./dist --slug app --spa         # deep links and refreshes reach the app's router
```

A single-page app draws its pages in the browser from one `index.html`, so there is no file at
`/users/42`: a link to it, or a refresh on it, is a 404. `--spa` turns on the fallback — a page
path with nothing published at it answers with the root `index.html`, and the router takes it from
there. A missing script or image still 404s.

- **Only for an app that routes in the browser** (React Router, Vue Router and the like). Not for
  a static site, docs, a report or Markdown, where every page is a file: there the fallback makes
  a dead or mistyped link open the home page instead of a 404, and nobody sees that it is broken.
  An app on hash routes (`/#/users/42`) needs nothing.
- **Build for the address.** On a workspace host the site lives under `/<slug>/`: build with that
  base (`vite build --base=/app/`), give the router the same basename, and fix the slug with
  `--slug`, since the build now depends on it. On its own domain (`--domain`) the base is `/`. The
  usual blank page is a build with base `/` on a workspace host: every script 404s. A relative
  `./` breaks on any page two levels deep.
- It is a setting of the site, like its visibility. Left off, a republish keeps it, so pass `--spa`
  on the first publish and not again. `--spa=off` turns it off — with the `=`; `--spa off` is
  refused. `colophon spa <slug> on|off` changes it without publishing. Once the site exists it is
  an owner's to change, and a draft or a version in review leaves it as it is; the CLI says so.
- A preview has a host of its own, with the site at the path it lives at:
  `https://p<version id>.usercontent.colophon.fyi/app/`. So a built app's `--draft` or `--review`
  loads its own scripts there, and its router reads its own paths: the person or a reviewer
  clicks through it as it will be live. Hand over the URL the CLI printed; never build a preview
  address yourself. One of the older form, `/app/_v/<id>/`, sends the reader on to the version's
  own host.

A `_redirects` file at the root of what you publish moves or rewrites paths, one
`from to [status]` rule a line, as Netlify reads it (Vite copies `public/_redirects` there):

```
/old-page        /new-page
/blog/:slug      /posts/:slug        302
/docs/*          /v2/docs/:splat
```

- **When a republish moves or renames a page, add a rule from the old path**, and tell the person:
  links already handed out keep working, which is what a fixed slug was for.
- Paths are the site's own: `/new-page` is `/<slug>/new-page` on a workspace host. Never write
  the slug into a rule.
- `301` is the default; `302`, `307` and `308` redirect too, `200` answers with another file of
  the site, and `!` after the status applies the rule even where a file exists. Otherwise a file
  at the path wins, so a build's own `/* /index.html 200` works as a fallback here as on Netlify.
  No query-parameter matching, no conditions (`Country=`, `Role=`), no proxying another host.
- It is read at publish: stderr says `3 rules from _redirects`, and a line that is wrong fails the
  publish with `_redirects line 4: …` saying what. Fix that line; do not drop the file to get the
  publish through. A target on another host is checked like a page's links, and a flagged one
  holds the version.

## Sending it for review

```bash
colophon publish ./report --slug report --review --note "Q3 numbers in; check the revenue chart"
colophon versions report     # review states, then the version in review and the last decision
colophon review report 3 --note "Put back v3: v4 broke the chart"
```

`--review` stores the version without putting it live and asks for a decision on it. The
workspace's publishers and owners are mailed, and so is a client the site is shared with at
**Can approve** (below). One of them approves it, which makes it live, or asks for changes with a
note. stdout is the version's preview URL, not the site's; stderr says `in review, not live` and
gives the site's URL. Give the person both, and say who was asked.

- **When to send for review rather than publish live:** when someone other than the person you
  work for has to agree first — "let Priya check it before it goes out", "the client signs off" —
  or the person asks for a review. Not by default: it waits on people who were not expecting to be
  asked. `--draft` is for the person to look first themselves; nobody is told about a draft.
- **Write the note for whoever decides**, a client included, who reads it on the page: what
  changed and what to look at, up to 2000 characters.
- Like a draft, it leaves an existing site as it is: its visibility, password, expiry and `--spa`
  do not change with it.
- **One version per site is in review at a time.** Sending a newer one replaces it, and reviewers
  are mailed once per round. So revising is: read the decision, fix, publish with `--review`
  again — the same slug, never a second site.
- **Reading the decision:** `colophon versions <slug>` ends each line with its review state
  (`in review`, `changes requested`, `approved`, `superseded`), then names the version in review
  and the last decision with its note — `changes requested on v4 by Priya: “Shorter intro”`. That
  note is what to fix. A review waits on a person: look when the person asks or comes back, not
  in a loop.
- `colophon review <slug> <n>` sends a version already published — a draft, or an earlier one to
  put back — the same way, and leaves the version already in review as it is, saying so.
- **Approving is a person's sign-off, never yours.** There is no approve command. A publisher or
  owner approves in the site's **Review** panel in the dashboard (**Approve and make live**), a
  client at Can approve on the page. Do not approve by `make-live` either: a version in review made live that
  way is approved in the name of whoever's login ran it. When the person asking you to put it live
  is the one who would approve, send them to the **Review** panel: one click, and the approval,
  with their note, is theirs.

### A workspace that requires approval

An owner can turn on **Approval before going live** under **Members & settings**. From then on a
publish from an API key, or from anyone below owner, goes into review instead of live, with or
without `--review`: stdout is the preview URL, and stderr says `in review, not live — this
workspace needs approval before a version goes live`. Owners are not held to it.

- **It is not a failure.** Do not retry, republish with other flags, or look for a credential the
  rule does not hold. Tell the person it waits on a publisher's or an owner's approval, and give
  them the preview URL. A publisher who sent it themselves cannot approve it; someone else does.
- `make-live` is for owners only there; anyone else, and every key, is told `… only an owner can
  make one live directly. Send it for review instead`. "Undo that" is then `colophon review <slug>
  <n>` with a note saying why, and a reviewer puts it back.
- A publish there that names a new visibility, expiry, password or `--spa` for an existing site is
  refused (`… a version in review leaves 'report' as it is: its visibility cannot change with
  it`). Publish without them; changing them is an owner's, on the site.
- Do not ask the person to turn the rule off, or for an owner's login, to get past it: it is there
  so that a person decides what goes live.

### A client who signs off

On a `restricted` site, someone outside the workspace can be the one who approves: shared at
**Can approve** under **Shared with**, by their own address, never a domain. They are mailed when
a version is sent for review, sign in, read the note, and approve or ask for changes on the page
itself. One approval is enough, so theirs puts the version live without anyone in the workspace.
That is why it is granted only when the person asks for the client to sign off, and only by an
owner: in the dashboard, or over MCP with `share_site` and `role: "approver"`. The CLI has no
command for it. `versions` names them as one: `approved on v4 by <name> (outside approver,
<address>)`.

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
  thing it was there to prevent. A version sent for review is not a draft to make live: approving
  it does that, and approving is not yours ([above](#sending-it-for-review)).
- In a workspace that requires approval only an owner runs `make-live`. Below owner, an earlier
  version goes back by `colophon review <slug> <n>` and a reviewer's approval.
- Tell them what moved. stdout is the URL; stderr says `v2 is live in place of v3: ~1 -1`, or
  `v2 was already live; nothing changed`.
- A version held by Colophon's content check cannot be made live — a Colophon admin releases or
  rejects it — and one rejected there never can. Say so; do not retry. The CLI calls these
  `held for review` and `rejected in review`; they are not the workspace's own review, and nobody
  in the workspace can approve them.
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
address under **Shared with** — the person does not need an account first. At the page they sign
in with Google, GitHub, a Microsoft work or school account, or a link mailed to them; what lets
them in is the address, not the way they signed in. A Microsoft account whose address Microsoft
has not confirmed is turned away, and the mailed link still works. Each is **Can view**,
**Can comment** or **Can approve**, the last for a client who signs off
([above](#a-client-who-signs-off)).

A workspace's owner can cap how open any site may be. A level above the cap is refused, with the
levels it allows; a new site published with no `--visibility` lands at the most open of those that
needs no password, and stderr says so. Ask the person which of the allowed levels they want rather
than picking one.

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

## Knowing who read it

"Has the client opened it?" has an answer only on a `restricted` or `private` site: the reader
signed in to open it, so Colophon knows who. `public`, `unlisted` and `password` sites count
visitors and never name one. When the person wants to know who opens a page, that is the reason
to choose `restricted`; say so when they pick a level.

- **Opened by**, on the site's page in the dashboard, for publishers and owners: everyone who
  opened it, how many visits, the version they last saw (the live one, an earlier one, or the one
  sent for review), and how long they have read and how far down they got — "read 4 min,
  scrolled to 100%". Below it, the people it was shared with who have not opened it yet.
- **A mail when it happens.** The first time someone opens a restricted or private site, and the
  first time they open a version they had not seen — a new live version, or the one sent for
  review — whoever published the live version and whoever sent a version for review are mailed,
  naming the reader and the version. So "tell me when the client opens it" needs nothing set up.
  A site published with an API key mails whoever made the key; when nobody who published it may
  see who opened it, the workspace's owners are mailed instead. Opens a few minutes apart come as
  one mail, nobody is mailed twice about the same person and version, and the workspace's
  notification channel, if it has one, hears it too.
- **Turning it off, or on, is each person's own setting**, and theirs to ask for. On the site's
  page, **Opened by** has **Stop mailing me** and **Mail me** (on also works for a site they did
  not publish); **Notifications** turns it off for every site in the workspace. The CLI has no
  command for it. An agent connected over MCP calls `set_read_alerts` (`mail`, and `slug` for
  one site); the API is `PUT /api/v1/sites/:id/read-alerts` with `{"mail": false}`. Both act for
  a signed-in person and refuse an API key, which is nobody to mail — with only a key, send the
  person to the dashboard.

How a page was read, on any site: when a reader leaves a page, the analytics beacon reports how
many seconds it was in front of them (up to 30 minutes a view) and how far down they scrolled, in
quarters of the page. The site's **Reading** card shows each page's median time and how many reads
got 25, 50, 75 and 100% of the way down; the stats API (`GET /api/v1/stats/sites/:id`, under
`engagement`) and the MCP tool `site_stats` give the same numbers. Like the view counts this is
anonymous — no cookie, no new identifier — except on restricted and private sites, where it is
also added to that reader's line under **Opened by**. Details at
https://colophon.fyi/docs/analytics#reading and https://colophon.fyi/docs/access#alerts.

## Publishing from CI

When the person wants a site published from CI — docs on every push to main, a report a scheduled
job rebuilds — it is one step: this CLI through `npx`, pinned, with the key from a secret. In
GitHub Actions:

```yaml
- id: site
  run: |
    url=$(npx -y @strangenoob/colophon@0.15.0 publish ./dist --slug docs --visibility unlisted)
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
- In a workspace that [requires approval](#a-workspace-that-requires-approval), every run's publish
  goes into review: the step passes, and the URL it keeps is that version's preview, not the site.
  It goes live when someone approves it. Tell the person when you set the workflow up.

There is no Colophon GitHub Action to `uses:`; this step is the supported way. Details at
https://colophon.fyi/docs/cli#ci.

## Their own domain

A workspace can answer on a hostname of its own — `https://m.example.dev/report/` instead of
`https://acme.usercontent.colophon.fyi/report/`. Once it is live, that is the URL `publish` and
`list` print; the subdomain form keeps working too. Hand the person whichever the CLI printed —
both are correct.

Attaching one is an owner's job in the dashboard (**Members & settings → Workspace settings**),
not something you can do from the CLI. If the person asks for their sites on their own domain,
tell them where, and what to expect: they type the hostname, get two DNS records to add (a TXT
that proves it is theirs and a CNAME to `edge.usercontent.colophon.fyi`, the same for every
workspace), and their URLs switch on their own once both resolve — nothing needs republishing.
A CNAME to the workspace's own subdomain, the old target, no longer reaches it; the dashboard
says the record needs the new value. Details at https://colophon.fyi/docs/workspaces#domain.

## Other commands

```bash
colophon list                        # slug, visibility and URL for every site
colophon search <words>              # which live page says it, across every site in the workspace
colophon versions <slug>             # every version, newest first: what each changed, and its review
colophon versions <slug> --diff 2    # what making v2 live would change against what is live now
colophon review <slug> 2 --note "…"  # send v2 for review: a draft, or an earlier version to put back
colophon make-live <slug> 2          # make v2 the live version: a rollback, or a draft approved
colophon visibility <slug> <level>   # change who can open a site without republishing it
colophon expire <slug> <moment>      # when it stops answering: 410 on every path, nothing deleted
colophon expire <slug> none          # clear that, so it answers again
colophon spa <slug> on|off           # the single-page-app fallback, without republishing
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
  `publish` or `make-live`: the person's role lets them propose, not put live. Publish with
  `--review` and a `--note` (for `make-live`, `colophon review <slug> <n>`): the workspace's
  publishers and owners are asked, and one of them approves it. Do not ask them to change roles.
- `publishing drafts needs the editor role or above`, or `sending a version for review needs the
  editor role or above` — the person can read and comment, not propose. Say who can.
- `in review, not live — this workspace needs approval before a version goes live` — not an error;
  the publish worked and waits on a person ([above](#a-workspace-that-requires-approval)). On
  `make-live`, `… only an owner can make one live directly`: send it with `colophon review`
  instead. On a republish, `… its visibility cannot change with it` (or expiry, password,
  single-page-app fallback): publish without that flag.
- `… needs the owner role or above` on `visibility`, `expire`, `spa` or `delete`, or `changing an
  existing site's visibility is for owners` (or `password is for owners`, or `single-page-app
  fallback on is for owners`) on a republish — those are an owner's decisions. Republish without
  `--visibility`, `--password-stdin` or `--spa` to keep the site as it is, and say who can change it.
- `'report' cannot be public: this workspace allows no site more open than unlisted` — the
  workspace's sharing limit. Tell the person, offer the levels the message lists, and say that
  raising the limit is an owner's, under **Members & settings**.
- `visibility 'password' needs a password for readers to type` — the level went without one.
  Ask the person for it and pipe it in with `--password-stdin`.
- `password must be at least 6 characters`, `… cannot start or end with a space` — ask for
  another. `--password-stdin read nothing` — the pipe was empty. `--password would leave it in
  your shell history` — pipe it instead.
- `quota exceeded: sites (4 > 3)` — the plan's site limit. Either `colophon delete` a site
  that is finished with, or the person upgrades. Do not delete one to make room on your own.
- `archive contains no files` — the directory is empty, or everything in it was skipped.
- `held for review` — Colophon's content check stored the upload without putting it live, and an
  admin releases or rejects it. Not the workspace's review: nobody in it can approve this. Say so;
  do not retry.
- `… is held for review and cannot be made live` or `… was rejected in review` on `make-live` —
  that version cannot be put live this way. Say so, and offer an earlier version instead. On
  `review`, the same versions answer `… cannot be reviewed until an admin releases it` or
  `… can never go live`, and the live one `… is the live version already`.
- `_redirects line 4: …` — that line of the file is wrong, and the message says how. Fix it and
  publish again; nothing was stored.
- `write --spa=off: --spa alone turns it on` — `--spa off` reads as two arguments. Write it with
  the `=`.
- `--review already stores the version as a draft` — pass one of `--draft` and `--review`.
  `--note goes with --review` — a note is for reviewers, so it needs `--review`.
- `no version 9 of <slug>` — the number is not one `colophon versions <slug>` prints. Run it and
  pick again.

## Notes

- Docs live at https://colophon.fyi/docs — the sign-in flow is /docs/signin, the CLI reference
  /docs/cli, access levels /docs/access. Link to them instead of paraphrasing when the person
  wants detail.
- If the person asks how to get this skill into Codex, Cursor, Gemini CLI, Copilot, OpenCode or
  another agent: `colophon skill install` detects what is on the machine and installs
  into each; `colophon skill install codex` picks one. Details at https://colophon.fyi/docs/skill.

- Every published page carries a small analytics beacon. Views, referrers, devices, time on page
  and scroll depth show up under the site in the dashboard. No cookies are set, and no visitor is
  identified except the signed-in readers of a restricted or private site (see
  [Knowing who read it](#knowing-who-read-it)).
- `COLOPHON_API` overrides the API origin for a self-hosted instance.
