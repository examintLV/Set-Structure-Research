import tempfile
import unittest
from pathlib import Path
from validate_records import validate

class ValidatorTests(unittest.TestCase):
    def make(self, content):
        f = tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", delete=False)
        f.write(content); f.close()
        self.addCleanup(lambda: Path(f.name).unlink(missing_ok=True))
        return Path(f.name)

    def test_valid(self):
        p = self.make("match_id,match_date,discipline,surface,match_format,status\nm1,2025-01-01,singles,hard,best-of-three,completed\n")
        self.assertEqual(validate(p), [])

    def test_duplicate(self):
        p = self.make("match_id,match_date,discipline,surface,match_format,status\nm1,2025-01-01,singles,hard,best-of-three,completed\nm1,2025-01-02,singles,clay,best-of-three,completed\n")
        self.assertTrue(any("duplicate" in e for e in validate(p)))

    def test_walkover_separate(self):
        p = self.make("match_id,match_date,discipline,surface,match_format,status\nm2,2025-01-01,singles,hard,best-of-three,walkover\n")
        self.assertTrue(any("walkover" in e for e in validate(p)))

if __name__ == "__main__":
    unittest.main()
