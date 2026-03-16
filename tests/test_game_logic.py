from logic_utils import (
    check_guess,
    parse_guess,
    get_temperature_hint,
    load_high_score,
    save_high_score,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_numeric_comparison_not_lexicographic():
    # Regression: ensure comparisons are numeric, not string-based.
    result = check_guess(9, 10)
    assert result == "Too Low"


def test_parse_guess_negative_number():
    ok, guess, err = parse_guess("-5")
    assert ok is True
    assert guess == -5
    assert err is None


def test_parse_guess_decimal_rejected_if_not_whole():
    ok, guess, err = parse_guess("5.7")
    assert ok is False
    assert guess is None
    assert err == "Please enter a whole number."


def test_parse_guess_extremely_large_value():
    ok, guess, err = parse_guess("999999999999999999999999")
    assert ok is True
    assert guess == 999999999999999999999999
    assert err is None


def test_temperature_hint_ranges():
    assert get_temperature_hint(50, 50) == "🎯 Exact match"
    assert get_temperature_hint(49, 50) == "🔥 Very hot"
    assert get_temperature_hint(45, 50) == "🌤 Warm"
    assert get_temperature_hint(40, 50) == "❄️ Cool"
    assert get_temperature_hint(1, 50) == "🧊 Ice cold"


def test_high_score_persistence(tmp_path):
    high_score_file = tmp_path / "high_score.txt"
    assert load_high_score(high_score_file) == 0

    save_high_score(123, high_score_file)
    assert load_high_score(high_score_file) == 123
