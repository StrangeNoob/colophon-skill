# colophon — an agent skill

Colophon teaches coding agents to publish a directory and return one governed, versioned URL. The
same `SKILL.md` is packaged as an open [Agent Skill](https://agentskills.io), a portable
[Agent Plugin](https://agent-plugins.org), and native Claude Code and Codex plugins.

## Install

Install through the cross-agent Skills CLI and choose the agents you use:

```bash
npx --yes skills add StrangeNoob/colophon-skill --skill colophon -g
```

Or install through Colophon's own CLI:

```bash
npm install -g @strangenoob/colophon
colophon skill install
```

`colophon skill install` detects its supported clients: Claude Code, Codex, Cursor, Gemini CLI,
GitHub Copilot, OpenCode, Windsurf, Cline, and Amp. Claude Code receives the plugin; the other
selected clients are handed to the cross-agent Skills CLI. That CLI uses symlinks by default and
can be run again to update the installation.

Other installation routes:

- Agent Plugin clients can install this public repository directly.
- GitHub CLI 2.90 or later can install the skill with
  `gh skill install StrangeNoob/colophon-skill colophon --agent <agent> --scope user`.
- Manual installations can copy `skills/colophon` to `~/.agents/skills/colophon`.
- Claude Code users can run `claude plugin marketplace add StrangeNoob/colophon-skill`, followed by
  `claude plugin install colophon@colophon`.

## What it needs

Install the [`@strangenoob/colophon`](https://www.npmjs.com/package/@strangenoob/colophon) CLI and
sign in:

```bash
npm install -g @strangenoob/colophon
colophon login
```

On a headless machine—CI, a server, or a sandbox without a browser—set an API key in
`COLOPHON_TOKEN`. Mint one with `colophon create-token --name <agent>` from your own machine. See
[Signing in](https://colophon.fyi/docs/signin) for the complete authentication flow.

## What the skill teaches

- Publish a directory with `colophon publish <dir>` and return its URL.
- Re-publish the same slug to update a site without changing its URL.
- Choose between `public`, `unlisted`, `restricted`, and `private` visibility.
- Check `colophon whoami` before publishing and keep credentials out of chat.
- Explain operational failures without deleting an existing site on the user's behalf.

See [PUBLISHING.md](PUBLISHING.md) for release and marketplace instructions. Product documentation
lives at [colophon.fyi/docs](https://colophon.fyi/docs).

MIT © StrangeNoob
