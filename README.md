# colophon — Claude Code skill

Teaches an agent to publish a directory to the web and hand back one governed, versioned URL.

```
/plugin marketplace add StrangeNoob/colophon-skill
/plugin install colophon
```

Then the agent reaches for it whenever it has produced files that a person needs a link to —
a report, a chart, a slide deck, a rendered page.

## What it teaches

- `colophon publish <dir>` and the flags that matter
- that re-publishing the same slug **replaces what is live and keeps the URL**, so a link
  already given to someone stays correct — rather than publishing a second site per draft
- which of `public` / `unlisted` / `restricted` / `private` fits the request, and that the
  restricted ones make the reader sign in first
- to stop and ask for an API key rather than guessing, because only a person can create one
- what each failure means, including quota limits — and not to delete someone's site to make
  room on its own initiative

## The CLI

The skill drives [`@strangenoob/colophon`](https://www.npmjs.com/package/@strangenoob/colophon):

```bash
npm install -g @strangenoob/colophon
export COLOPHON_TOKEN=colo_live_…     # app.colophon.fyi → Keys
colophon publish ./report --name "Q3 report"
```

Node 18+. Point `COLOPHON_API` at your own instance if you self-host.

## Without the plugin system

Copy the skill straight in:

```bash
git clone https://github.com/StrangeNoob/colophon-skill
cp -R colophon-skill/skills/colophon ~/.claude/skills/colophon
```

MIT © StrangeNoob
