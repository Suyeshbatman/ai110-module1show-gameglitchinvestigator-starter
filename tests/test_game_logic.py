# FIX: Bug 10 — Tests were broken: stubs raised NotImplementedError and assertions
# compared tuples to bare strings. Rewritten with full coverage for all 4 functions.

from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


# ── TestGetRangeForDifficulty ────────────────────────────────────────────────

class TestGetRangeForDifficulty:
    def test_easy_range(self):
        assert get_range_for_difficulty("Easy") == (1, 20)

    def test_normal_range(self):
        assert get_range_for_difficulty("Normal") == (1, 100)

    def test_hard_range(self):
        assert get_range_for_difficulty("Hard") == (1, 200)

    def test_hard_is_harder_than_normal(self):
        """Regression for Bug 1: Hard range must be wider than Normal."""
        _, hard_high = get_range_for_difficulty("Hard")
        _, normal_high = get_range_for_difficulty("Normal")
        assert hard_high > normal_high

    def test_unknown_difficulty_returns_default(self):
        assert get_range_for_difficulty("Extreme") == (1, 100)

    def test_case_sensitivity(self):
        """Difficulty strings are case-sensitive; lowercase falls to default."""
        assert get_range_for_difficulty("easy") == (1, 100)


# ── TestParseGuess ───────────────────────────────────────────────────────────

class TestParseGuess:
    def test_valid_integer(self):
        assert parse_guess("42") == (True, 42, None)

    def test_negative_number(self):
        assert parse_guess("-7") == (True, -7, None)

    def test_decimal_truncated(self):
        assert parse_guess("3.9") == (True, 3, None)

    def test_none_input(self):
        ok, val, err = parse_guess(None)
        assert ok is False
        assert err == "Enter a guess."

    def test_empty_string(self):
        ok, val, err = parse_guess("")
        assert ok is False
        assert err == "Enter a guess."

    def test_non_numeric(self):
        ok, val, err = parse_guess("abc")
        assert ok is False
        assert err == "That is not a number."

    def test_extremely_large_value(self):
        ok, val, _ = parse_guess("999999999999")
        assert ok is True
        assert val == 999999999999

    def test_zero(self):
        assert parse_guess("0") == (True, 0, None)

    def test_whitespace_only(self):
        ok, val, err = parse_guess("   ")
        assert ok is False
        assert err == "That is not a number."

    def test_mixed_input(self):
        ok, val, err = parse_guess("12abc")
        assert ok is False
        assert err == "That is not a number."


# ── TestCheckGuess ───────────────────────────────────────────────────────────

class TestCheckGuess:
    def test_correct_guess(self):
        outcome, msg = check_guess(50, 50)
        assert outcome == "Win"
        assert "Correct" in msg

    def test_guess_too_high(self):
        outcome, msg = check_guess(60, 50)
        assert outcome == "Too High"

    def test_guess_too_low(self):
        outcome, msg = check_guess(40, 50)
        assert outcome == "Too Low"

    def test_hint_direction_too_high_says_lower(self):
        """Regression for Bug 2: When guess is too high, hint must say LOWER."""
        _, msg = check_guess(60, 50)
        assert "LOWER" in msg

    def test_hint_direction_too_low_says_higher(self):
        """Regression for Bug 2: When guess is too low, hint must say HIGHER."""
        _, msg = check_guess(40, 50)
        assert "HIGHER" in msg

    def test_boundary_off_by_one_high(self):
        outcome, _ = check_guess(51, 50)
        assert outcome == "Too High"

    def test_boundary_off_by_one_low(self):
        outcome, _ = check_guess(49, 50)
        assert outcome == "Too Low"

    def test_negative_numbers(self):
        outcome, _ = check_guess(-5, -3)
        assert outcome == "Too Low"

    def test_large_numbers(self):
        outcome, _ = check_guess(1000000, 999999)
        assert outcome == "Too High"


# ── TestUpdateScore ──────────────────────────────────────────────────────────

class TestUpdateScore:
    def test_win_first_attempt(self):
        """Attempt 1 win: 100 - 10*1 = 90 points added."""
        assert update_score(0, "Win", 1) == 90

    def test_win_fifth_attempt(self):
        """Attempt 5 win: 100 - 10*5 = 50 points added."""
        assert update_score(0, "Win", 5) == 50

    def test_win_minimum_10_points(self):
        """Even at attempt 100, minimum win bonus is 10."""
        assert update_score(0, "Win", 100) == 10

    def test_win_bug8_regression(self):
        """Regression for Bug 8: No +1 in formula. Attempt 1 → 90, not 80."""
        score = update_score(0, "Win", 1)
        assert score == 90

    def test_too_high_deducts_5(self):
        assert update_score(100, "Too High", 1) == 95

    def test_too_low_deducts_5(self):
        assert update_score(100, "Too Low", 1) == 95

    def test_bug7_regression_even_odd_consistent(self):
        """Regression for Bug 7: 'Too High' must deduct same amount on even and odd attempts."""
        score_even = update_score(100, "Too High", 2)
        score_odd = update_score(100, "Too High", 3)
        assert score_even == score_odd

    def test_score_can_go_negative(self):
        assert update_score(0, "Too Low", 1) == -5

    def test_unknown_outcome_no_change(self):
        assert update_score(50, "Unknown", 1) == 50
