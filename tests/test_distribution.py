"""Validate the package contracts consumed by skill and plugin installers."""

import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


class DistributionPackageTests(unittest.TestCase):
    def test_portable_manifest_matches_official_schema(self):
        jsonschema.Draft202012Validator(
            load_json("tests/agent-plugin.schema.json")
        ).validate(load_json("plugin.json"))

    def test_plugin_formats_keep_the_same_release_identity(self):
        portable = load_json("plugin.json")
        self.assertRegex(portable["version"], r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
        for path in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            with self.subTest(path=path):
                manifest = load_json(path)
                for field in ("name", "version", "license"):
                    self.assertEqual(manifest[field], portable[field])

    def test_skill_frontmatter_is_discoverable(self):
        skills = list((ROOT / "skills").glob("*/SKILL.md"))
        self.assertTrue(skills, "The plugin must contain at least one skill")
        for path in skills:
            with self.subTest(path=path):
                parts = path.read_text(encoding="utf-8").split("---", 2)
                self.assertEqual(parts[0], "")
                self.assertEqual(len(parts), 3)
                frontmatter = yaml.safe_load(parts[1])
                self.assertEqual(frontmatter["name"], path.parent.name)
                self.assertRegex(frontmatter["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertLessEqual(len(frontmatter["name"]), 64)
                description = frontmatter["description"]
                self.assertIsInstance(description, str)
                self.assertTrue(description.strip())
                self.assertLessEqual(len(description), 1024)
                self.assertTrue(parts[2].strip())

    def test_codex_references_resolve_inside_package(self):
        manifest = load_json(".codex-plugin/plugin.json")
        interface = manifest["interface"]
        paths = [manifest["skills"]]
        paths.extend(interface[field] for field in ("composerIcon", "logo", "logoDark") if field in interface)
        for relative_path in paths:
            with self.subTest(path=relative_path):
                self.assertTrue(relative_path.startswith("./"))
                path = (ROOT / relative_path).resolve()
                path.relative_to(ROOT.resolve())
                self.assertTrue(path.exists(), f"Missing package resource: {path}")
                if path.suffix == ".svg":
                    self.assertEqual(ET.parse(path).getroot().tag, "{http://www.w3.org/2000/svg}svg")
                elif path.suffix == ".png":
                    self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
        prompts = interface["defaultPrompt"]
        self.assertIsInstance(prompts, list)
        self.assertTrue(1 <= len(prompts) <= 3)
        self.assertTrue(all(isinstance(prompt, str) and 0 < len(prompt) <= 128 for prompt in prompts))


if __name__ == "__main__":
    unittest.main()
