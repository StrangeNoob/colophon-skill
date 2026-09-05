# colophon — an agent skill

Teaches a coding agent to publish a directory to the web and hand back one governed,
versioned URL. One `SKILL.md` in the open [Agent Skills](https://agentskills.io) format, so the
same skill works in Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode and any
other agent that reads skills.

## Install

```bash
npm install -g @strangenoob/colophon
colophon skill install
```

Finds every coding agent on your machine — Claude Code, Codex, Cursor, Gemini CLI, GitHub
Copilot, OpenCode and more — and installs the skill into each. Name agents to be selective:
`colophon skill install codex cursor`. Claude Code gets it as a plugin so it updates itself;
the others get a copy placed by the cross-agent installer, `npx skills`. Run it again to update.

By hand: `claude plugin marketplace add StrangeNoob/colophon-skill && claude plugin install
colophon@colophon` for Claude Code, `npx skills add StrangeNoob/colophon-skill -g` for the
rest, or copy `skills/colophon` into `~/.agents/skills/colophon`.

## What it needs

The [`@strangenoob/colophon`](https://www.npmjs.com/package/@strangenoob/colophon) CLI, signed
in:

```bash
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
