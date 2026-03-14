def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        # FIX: Bug 1 — Hard range was (1, 50), which is easier than Normal (1, 100).
        # Normal changed to (1, 50) and Hard Changed to (1, 100) so Hard is genuinely harder.
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: Bug 2 — Hint messages were backwards ("Go HIGHER!" when guess was too high).
    # Swapped so "Too High" says "Go LOWER!" and "Too Low" says "Go HIGHER!".
    # Also removed the dead-code TypeError fallback (no longer needed after Bug 3 fix
    # ensures secret is always an int).
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIX: Bug 8 — Formula used (attempt_number + 1), over-penalizing the player.
        # Removed the +1 so score = 100 - 10 * attempt_number.
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # FIX: Bug 7 — "Too High" scoring was inconsistent: +5 on even attempts, -5 on odd.
    # Now always deducts 5 for any wrong guess, matching "Too Low" behavior.
    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
