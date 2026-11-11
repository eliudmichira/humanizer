import json
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from humanizer_audit import audit  # noqa: E402

SLOP = (
    "Founded in 2014, Brightline Coffee stands as a testament to Nairobi's vibrant café "
    "culture. The roastery boasts a diverse array of single-origin beans, showcasing its "
    "commitment to quality, sustainability, and community. Industry observers have noted "
    "its growing influence, highlighting its pivotal role in the evolving specialty-coffee "
    "landscape. Despite these successes, Brightline faces several challenges, including "
    "rising costs. Overall, it's not just a coffee shop — it's a movement."
)
PLAIN = "Brightline Coffee is a roastery in Nairobi, founded in 2014. It sells single-origin beans. Its costs are rising."


def cats(text):
    return {f["category"] for f in audit(text)["findings"]}


class AuditTests(unittest.TestCase):
    def test_dense_text_scores_high(self):
        report = audit(SLOP)
        self.assertEqual(report["band"], "high")
        for expected in ("significance", "copula", "ing_tail", "challenges",
                         "conclusion", "parallelism", "vocabulary", "triplet"):
            self.assertIn(expected, cats(SLOP))

    def test_plain_text_is_clean(self):
        report = audit(PLAIN)
        self.assertEqual(report["findings"], [])
        self.assertEqual(report["band"], "low")

    def test_code_and_urls_are_not_scanned_as_prose(self):
        text = (
            "Run `leverage --robust` first.\n\n"
            "```sh\n# it serves as a testament, highlighting nothing\n```\n\n"
            "See https://example.org/pivotal-landscape for details.\n"
        )
        self.assertEqual(audit(text)["findings"], [])

    def test_tier_one_items(self):
        self.assertIn("residue", cats("Certainly! Here is a revised draft of the article."))
        self.assertIn("placeholder", cats("Founded in [Year] by [Founder Names]."))
        self.assertIn("placeholder", cats("|access-date=2025-XX-XX"))
        self.assertIn("artifact", cats("See https://a.org/x?utm_source=chatgpt.com for more."))

    def test_four_item_list_is_not_a_triplet(self):
        self.assertNotIn("triplet", cats("We sell tea, coffee, juice, and water."))
        self.assertIn("triplet", cats("We sell tea, coffee, and juice."))

    def test_line_numbers(self):
        report = audit("First line is fine.\n\nIt serves as a hub.\n")
        self.assertEqual([f["line"] for f in report["findings"]], [3])

    def test_cli_json_and_exit_code(self):
        cmd = [sys.executable, str(ROOT / "humanizer_audit.py"), "--json", "--fail-over", "1"]
        bad = subprocess.run(cmd + ["--text", SLOP], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)
        self.assertEqual(json.loads(bad.stdout)["band"], "high")
        good = subprocess.run(cmd + ["--text", PLAIN], capture_output=True, text=True)
        self.assertEqual(good.returncode, 0)


if __name__ == "__main__":
    unittest.main()
