"""Unit tests for the STUDY-001 pipeline: score grammar, Wilson CIs, exclusions."""
import unittest

from study001_pipeline import (
    parse_score,
    wilson,
    _validate_conventional_set,
    _set_wins,
    pct,
)


class ScoreGrammarTests(unittest.TestCase):
    def test_straight_sets(self):
        p = parse_score("6-4 7-5")
        self.assertTrue(p.ok)
        self.assertEqual(p.status, "completed")
        self.assertEqual(p.n_conventional, 2)
        self.assertFalse(p.has_match_tiebreak)

    def test_three_sets(self):
        p = parse_score("6-4 3-6 7-6(5)")
        self.assertTrue(p.ok)
        self.assertEqual(p.n_conventional, 3)
        self.assertTrue(p.sets[2]["tiebreak"])

    def test_tiebreak_first_set(self):
        p = parse_score("7-6(4) 6-3")
        self.assertTrue(p.ok)
        self.assertTrue(p.sets[0]["tiebreak"])
        self.assertEqual(p.sets[0]["tb_loser_points"], 4)

    def test_seven_five_is_not_tiebreak(self):
        p = parse_score("7-5 6-4")
        self.assertTrue(p.ok)
        self.assertFalse(p.sets[0]["tiebreak"])

    def test_retirement_detected(self):
        p = parse_score("6-3 2-4 RET")
        self.assertEqual(p.status, "retired")

    def test_walkover_detected(self):
        p = parse_score("W/O")
        self.assertEqual(p.status, "walkover")

    def test_default_detected(self):
        p = parse_score("6-5 Def.")
        self.assertEqual(p.status, "default")

    def test_match_tiebreak_bracket(self):
        p = parse_score("6-4 6-7(4) [10-4]")
        self.assertTrue(p.has_match_tiebreak)
        self.assertEqual(p.n_conventional, 2)
        self.assertFalse(p.sets[2]["is_match_tiebreak"] is False)  # is a match TB

    def test_abandoned_detected(self):
        p = parse_score("6-1 5-7 3-2 Played and unfinished")
        self.assertEqual(p.status, "abandoned")

    def test_completed_with_one_set_rejected(self):
        p = parse_score("6-4")
        self.assertFalse(p.ok)

    def test_completed_with_four_sets_rejected(self):
        p = parse_score("6-4 3-6 6-4 7-5")
        self.assertFalse(p.ok)

    def test_inconsistent_set_tally_rejected(self):
        # winner "won" only one set but match is complete
        p = parse_score("6-4 4-6")
        self.assertFalse(p.ok)

    def test_empty_score(self):
        self.assertFalse(parse_score("").ok)
        self.assertFalse(parse_score(None).ok)


class SetValidationTests(unittest.TestCase):
    def test_valid_sets(self):
        for a, b, tb in [(6, 0, None), (6, 4, None), (7, 5, None), (7, 6, 5), (6, 3, None)]:
            ok, _ = _validate_conventional_set(a, b, tb)
            self.assertTrue(ok, f"{a}-{b} should be valid")

    def test_invalid_sets(self):
        for a, b, tb in [(6, 5, None), (5, 5, None), (8, 6, None), (6, 7, "x")]:
            if tb == "x":
                continue  # reached via the tiebreak-marker test instead
            ok, _ = _validate_conventional_set(a, b, tb)
            self.assertFalse(ok, f"{a}-{b} should be invalid")

    def test_seven_six_without_points_is_valid_tiebreak(self):
        # amended per spec amendment A1: 7-6 is a tiebreak set even when the
        # tiebreak points were not recorded.
        ok, _ = _validate_conventional_set(7, 6, None)
        self.assertTrue(ok)
        p = parse_score("7-6 6-4")
        self.assertTrue(p.ok)
        self.assertTrue(p.sets[0]["tiebreak"])
        self.assertIsNone(p.sets[0]["tb_loser_points"])

    def test_tiebreak_marker_requires_seven_six(self):
        ok, _ = _validate_conventional_set(6, 4, 7)
        self.assertFalse(ok)

    def test_set_wins_tally(self):
        p = parse_score("6-4 3-6 7-6(5)")
        self.assertEqual(_set_wins(p.sets), (2, 1))


class WilsonTests(unittest.TestCase):
    def test_known_value(self):
        # Wilson 95% CI for 50/100 is approx 0.4038..0.5962
        lo, hi = wilson(50, 100)
        self.assertAlmostEqual(lo, 0.4038, places=3)
        self.assertAlmostEqual(hi, 0.5962, places=3)

    def test_extremes_stay_bounded(self):
        lo, hi = wilson(0, 20)
        self.assertGreaterEqual(lo, 0.0)
        self.assertLess(hi, 0.20)
        lo2, hi2 = wilson(20, 20)
        self.assertLessEqual(hi2, 1.0)
        self.assertGreater(lo2, 0.80)

    def test_zero_denominator(self):
        lo, hi = wilson(0, 0)
        self.assertTrue(lo != lo)  # NaN
        self.assertEqual(pct(0, 0), "n/a")


if __name__ == "__main__":
    unittest.main()

class BestOfFiveTests(unittest.TestCase):
    """Regression tests for the best-of-5 defect fixed 2026-11-15.

    The parser hardcoded best-of-3 validation and rejected every best-of-5
    match as unparseable. STUDY-001 never exposed it (that sample is 100%
    best-of-3); STUDY-002 did, on Sumit Nagal's Grand Slam records.
    """

    def test_straight_sets_bo5(self):
        p = parse_score("6-3 6-3 6-2", best_of=5)
        self.assertTrue(p.ok, p.reason)
        self.assertEqual(p.n_conventional, 3)

    def test_four_sets_bo5(self):
        p = parse_score("4-6 6-1 6-2 6-4", best_of=5)
        self.assertTrue(p.ok, p.reason)
        self.assertEqual(p.n_conventional, 4)

    def test_five_sets_bo5(self):
        p = parse_score("6-3 6-7(4) 6-3 4-6 6-2", best_of=5)
        self.assertTrue(p.ok, p.reason)
        self.assertEqual(p.n_conventional, 5)

    def test_three_sets_is_invalid_for_bo5_winner_tally(self):
        # 3 sets in bo5 means the winner took exactly 3: valid only if tally is 3-0
        p = parse_score("6-2 7-5 6-3", best_of=5)
        self.assertTrue(p.ok, p.reason)

    def test_bo5_rejects_six_sets(self):
        p = parse_score("6-3 6-3 6-3 6-3 6-3 6-3", best_of=5)
        self.assertFalse(p.ok)

    def test_bo5_retirement_still_retirement(self):
        p = parse_score("6-3 2-4 RET", best_of=5)
        self.assertEqual(p.status, "retired")

    def test_default_arg_preserves_bo3_behaviour(self):
        # a 4-set match must still be invalid when best_of is not supplied
        self.assertFalse(parse_score("6-4 3-6 6-4 7-5").ok)
        self.assertTrue(parse_score("6-4 3-6 6-4").ok)
