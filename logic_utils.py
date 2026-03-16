from pathlib import Path


HIGH_SCORE_FILE = Path("high_score.txt")


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive guessing range for the selected difficulty.

    Args:
        difficulty: A difficulty label such as "Easy", "Normal", or "Hard".

    Returns:
        A tuple of (low, high) bounds for the secret number range.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse a user-entered guess into an integer.

    The parser accepts standard integer text and integer-like decimals
    (for example, "5.0"). It rejects non-numeric values and decimal values
    with a fractional component (for example, "5.7").

    Args:
        raw: Raw text entered by the player.

    Returns:
        A tuple of (ok, guess_int, error_message).
        If parsing succeeds, ok=True and guess_int contains the parsed value.
        If parsing fails, ok=False and error_message explains the issue.
    """
    if raw is None:
        return False, None, "Enter a guess."

    cleaned = raw.strip()
    if cleaned == "":
        return False, None, "Enter a guess."

    try:
        # Accept integer-like decimals (e.g. 5.0) but reject 5.7.
        if "." in cleaned:
            as_float = float(cleaned)
            if not as_float.is_integer():
                return False, None, "Please enter a whole number."
            value = int(as_float)
        else:
            value = int(cleaned)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare a guess to the secret number and return the game outcome.

    Args:
        guess: The player's numeric guess.
        secret: The secret number to compare against.

    Returns:
        One of: "Win", "Too High", or "Too Low".
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number.

    Args:
        current_score: The player's score before this guess.
        outcome: The result label from ``check_guess``.
        attempt_number: The current attempt count after submitting a guess.

    Returns:
        The updated score integer.
    """
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score


def get_temperature_hint(guess: int, secret: int) -> str:
    """Return a hot/cold hint based on guess distance from the secret.

    Args:
        guess: The player's numeric guess.
        secret: The secret number.

    Returns:
        A short hint string such as "🔥 Very hot" or "🧊 Ice cold".
    """
    distance = abs(guess - secret)
    if distance == 0:
        return "🎯 Exact match"
    if distance <= 2:
        return "🔥 Very hot"
    if distance <= 5:
        return "🌤 Warm"
    if distance <= 10:
        return "❄️ Cool"
    return "🧊 Ice cold"


def load_high_score(path: Path = HIGH_SCORE_FILE) -> int:
    """Load the saved high score from disk.

    Args:
        path: File path used to persist the high score.

    Returns:
        The saved high score, or 0 when no score exists or data is invalid.
    """
    try:
        if not path.exists():
            return 0
        raw = path.read_text(encoding="utf-8").strip()
        return max(0, int(raw))
    except Exception:
        return 0


def save_high_score(score: int, path: Path = HIGH_SCORE_FILE) -> None:
    """Persist the high score to disk.

    Args:
        score: Score to store as the current best score.
        path: File path used to persist the high score.
    """
    path.write_text(str(max(0, int(score))), encoding="utf-8")
