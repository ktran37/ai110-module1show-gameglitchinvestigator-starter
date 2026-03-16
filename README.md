# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

### Purpose
This app is a Streamlit number guessing game where the player tries to guess a secret number within a limited number of attempts based on difficulty.

### Bugs Found
- Hint direction bug: "Too High" returned a message telling the player to go higher, and "Too Low" told the player to go lower.
- Type inconsistency bug: the app sometimes converted the secret number to a string before comparison, causing unreliable outcomes.
- Attempt tracking issue: attempts started from an inconsistent initial value, making attempts-left feedback confusing.

### Fixes Applied
- Refactored core logic out of app.py into logic_utils.py (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`).
- Fixed guess evaluation to always use numeric comparisons and return consistent outcomes (`Win`, `Too High`, `Too Low`).
- Corrected hint text mapping in the UI so guidance matches the actual guess result.
- Stabilized game state behavior for new games by resetting status/history/score and reusing the selected difficulty range.
- Added a regression test to confirm numeric comparison behavior and expanded edge-case coverage with pytest (`9 passed`).

## 📸 Demo

- [x] Fixed game runs and is winnable with correct hints.
- [x] Inserted screenshot: winning game screen with Developer Debug Info visible.

Optional screenshot target:
- `winning_game_screen.png`

![Winning game screenshot](winning_game_screen.png)

## 🚀 Stretch Features

- [x] Enhanced UI implemented with color-coded hints, hot/cold signals, and session summary table.
- [x] Enhanced UI screenshot included below.

If you complete Challenge 1 (Advanced Edge-Case Testing), add:
- [x] Added edge-case tests for negative numbers, non-integer decimals, and extremely large values.
- [x] Verified all tests pass with pytest (`9 passed`).
- [x] Inserted screenshot of pytest output showing Stretch 1 tests passing.

### Stretch 1 Notes
Edge-case tests were added in [tests/test_game_logic.py](tests/test_game_logic.py) to verify these inputs are handled gracefully:
- Negative number input (`-5`) parses correctly.
- Decimal input with fractional part (`5.7`) is rejected with a clear message.
- Extremely large integer input parses correctly without crashing.

Suggested screenshot filename:
- `stretch1-pytest-results.png`

![Stretch 1 pytest results](stretch1-pytest-results.png)

## ✅ Optional Challenge Progress

### Challenge 2: Feature Expansion via Agent Mode
- Implemented a persistent **High Score tracker** that saves best score to `high_score.txt`.
- Added a **Guess History summary table** in both main content and sidebar.
- Added collaboration notes in code near changes (for example, in `app.py` where high score state is initialized).

### Challenge 3: Professional Documentation and Linting
- Added professional docstrings to every function in `logic_utils.py`.
- Cleaned function behavior and naming for readability and consistency.
- Verified no file-level errors in updated files and all tests pass.

### Challenge 4: Enhanced Game UI
- Added color-coded feedback (`st.success`, `st.warning`, `st.info`) based on guess accuracy.
- Added hot/cold hinting with emoji states (`Very hot`, `Warm`, `Cool`, `Ice cold`).
- Added a structured session table showing attempt, guess, outcome, distance, and hot/cold feedback.

![Enhanced game UI](winning_game_screen.png)

### Challenge 5: AI Model Comparison
- Completed in `reflection.md` with a short comparison of Copilot vs ChatGPT outputs for a logic bug fix.
