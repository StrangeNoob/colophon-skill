# Publishing Colophon for coding agents

This repository is the single source for every distribution channel. Do not fork or copy the skill
into agent-specific repositories.

## Release checks

Run these from the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
npx --yes skills@1.5.23 add . --list
```

On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`.
The tests validate the portable manifest against the vendored, unmodified
[Agent Plugins 1.0.0 schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json),
skill frontmatter, release identity, and packaged asset references. They do not substitute for
loading the plugin in each host or running the publishing workflows.

Keep the versions in `plugin.json`, `.codex-plugin/plugin.json`, and
`.claude-plugin/plugin.json` identical. Update the release tag at the same time.

## GitHub Agent Skills and Copilot

GitHub CLI 2.90 or later can validate and publish every skill in this repository:

```bash
gh skill publish --dry-run
gh skill publish --tag v0.2.2
```

Commit and push the tested release commit before publishing. Do not publish from an unmerged
worktree: the release must point to the same commit that passed validation. Publication creates a
GitHub release and adds the `agent-skills` topic; the skill is also installable directly from the
default branch before a release exists. See the [GitHub CLI reference](https://cli.github.com/manual/gh_skill_publish).

To build a clean plugin archive from that commit (all three manifests share the same skill):

```bash
mkdir -p dist
git archive --format=zip --output=dist/colophon-plugin.zip HEAD \
  plugin.json .codex-plugin .claude-plugin skills assets LICENSE README.md PUBLISHING.md marketplace
```

The output excludes Git metadata, local credentials, virtual environments, and test caches.

## skills.sh and cross-agent installation

No separate submission is required. Keep the repository public and use the canonical installation
command in the README. The skills.sh directory derives discovery signals from Skills CLI installs;
successful installation does not prove that a listing has been indexed. See [Skills CLI](https://github.com/vercel-labs/skills).

## OpenAI Plugins Directory

Upload the clean archive as a skills-only plugin in the
[OpenAI plugin submission portal](https://platform.openai.com/plugins). Use:

- Name: **Colophon**
- Category: **Developer Tools**
- Website: <https://colophon.fyi>
- Support: <https://github.com/StrangeNoob/colophon-skill/issues>
- Short description: **Publish agent-made files to a stable URL.**
- Long description: **Publish HTML, reports, charts, slide decks, and other generated files to one
  governed URL. Update the same URL in place and choose who can open it.**

Use the three prompts in `.codex-plugin/plugin.json` as starter prompts. The five positive and three
negative cases in `marketplace/openai-evals.json` specify prompts, fixtures, and expected outcomes;
they are test specifications, not evidence of a live service test.

The portal requires a verified developer identity before it allows plugin creation or upload.
Before submitting, supply approved public privacy and terms URLs, select supported regions, and
provide dedicated reviewer credentials through the portal's private fields. As of September 5,
2026, `colophon.fyi/privacy` and `colophon.fyi/terms` redirect to
404 pages. The manifest intentionally omits those URLs until real policies are available.
Do not publish generated policy text as an approved legal policy or store reviewer credentials in
this repository. See [OpenAI submission requirements](https://developers.openai.com/plugins/deploy/submission).

Submission starts a review. It does not immediately publish the plugin; after approval, the
publisher releases it from the portal.

## Cursor Marketplace

Cursor reads the portable Agent Plugin manifest at `plugin.json`. Test the repository locally from
`~/.cursor/plugins/local/colophon`, reload Cursor, and confirm that the Colophon skill appears. Then
submit the public repository at <https://cursor.com/marketplace/publish>. This requires a signed-in
Cursor publisher account and review by Cursor; a valid manifest alone is not a public listing.
The PNG logo is at `assets/logo.png`. See [Cursor plugin documentation](https://prod.cursor.com/docs/plugins).

## Other Agent Skills clients

For Gemini CLI, OpenCode, Windsurf, Cline, Amp, and other compatible clients, publish no duplicate
package. Direct users to the Skills CLI, GitHub CLI, the root Agent Plugin, or the standard
`~/.agents/skills/colophon` directory supported by their client.
