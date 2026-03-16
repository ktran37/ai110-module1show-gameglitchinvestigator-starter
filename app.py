import random
import streamlit as st
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    get_temperature_hint,
    load_high_score,
    save_high_score,
)


def outcome_message(outcome: str) -> str:
    # FIXME: Logic breaks here in the original app when "Too High" says go HIGHER.
    # FIX: Hint direction corrected with Copilot-assisted refactor review.
    if outcome == "Win":
        return "🎉 Correct!"
    if outcome == "Too High":
        return "📉 Too high. Go LOWER!"
    if outcome == "Too Low":
        return "📈 Too low. Go HIGHER!"
    return ""

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "history_rows" not in st.session_state:
    st.session_state.history_rows = []

if "best_score" not in st.session_state:
    # FIX: Added with Copilot Agent-style refactor to persist best runs.
    st.session_state.best_score = load_high_score()

st.sidebar.metric("🏆 High Score", st.session_state.best_score)

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: New game now respects difficulty range and stable session state.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.history_rows = []
    st.session_state.score = 0
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIXME: Logic breaks here in the original code when secret flips to str.
        # FIX: Keep numeric comparison only; removed alternating int/str behavior.
        secret = st.session_state.secret

        outcome = check_guess(guess_int, secret)
        message = outcome_message(outcome)
        temp_hint = get_temperature_hint(guess_int, secret)
        distance = abs(guess_int - secret)

        st.session_state.history_rows.append(
            {
                "Attempt": st.session_state.attempts,
                "Guess": guess_int,
                "Outcome": outcome,
                "Distance": distance,
                "Hot/Cold": temp_hint,
            }
        )

        if show_hint:
            if outcome == "Win":
                st.success(message)
            elif distance <= 5:
                st.warning(f"{message} {temp_hint}")
            else:
                st.info(f"{message} {temp_hint}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            if st.session_state.score > st.session_state.best_score:
                st.session_state.best_score = st.session_state.score
                save_high_score(st.session_state.best_score)
                st.success("🏆 New high score saved!")
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

if st.session_state.history_rows:
    st.subheader("📊 Session Guess Summary")
    st.dataframe(st.session_state.history_rows, use_container_width=True)

    st.sidebar.subheader("Guess History")
    st.sidebar.dataframe(st.session_state.history_rows, use_container_width=True)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
