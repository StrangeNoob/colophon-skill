# colophon — an agent skill

Teaches a coding agent to publish a directory to the web and hand back one governed,
versioned URL. One `SKILL.md` in the open [Agent Skills](https://agentskills.io) format, so the
same skill works in Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode and any
other agent that reads skills.

## Install

**Claude Code** — as a plugin, so it updates itself:

```bash
claude plugin marketplace add StrangeNoob/colophon-skill
claude plugin install colophon@colophon
```

**Everything else** — the cross-agent installer detects the agents on your machine and puts
the skill where each one looks:

```bash
npx skills add StrangeNoob/colophon-skill -g
```

Pick one agent with `-a codex` or `-a cursor`, or install into all of them with `-a '*'`. By hand: copy `skills/colophon` into `~/.agents/skills/colophon`, the shared
location Codex and friends read, or into the agent's own skills directory.

## What it needs

The [`@strangenoob/colophon`](https://www.npmjs.com/package/@strangenoob/colophon) CLI on the
path, signed in:

```bash
npm install -g @strangenoob/colophon
colophon login          # opens the browser; approve once
```

On a headless machine — CI, a server, a sandbox with no browser — set an API key in
`COLOPHON_TOKEN` instead. Mint one with `colophon create-token --name <agent>` from your own
machine. How signing in works: <https://colophon.fyi/docs/signin>.

## What it teaches

- `colophon publish <dir>` and the flags that matter
- that re-publishing the same slug **replaces what is live and keeps the URL**, so a link
  already given to someone stays correct — rather than publishing a second site per draft
- which of `public` / `unlisted` / `restricted` / `private` fits the request, and that the
  restricted ones make the reader sign in first
- to check `colophon whoami` first and, if nothing is signed in, to stop and ask the person to
  run `colophon login` — never to ask for a key when a login would do
- what each failure means, including quota limits — and not to delete someone's site to make
  room on its own initiative

Docs: <https://colophon.fyi/docs>. MIT © StrangeNoob
