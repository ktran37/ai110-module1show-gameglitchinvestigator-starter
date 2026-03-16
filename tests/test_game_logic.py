from logic_utils import check_guess, parse_guess

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
