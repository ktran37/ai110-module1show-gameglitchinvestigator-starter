# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

When I first ran the app, it loaded and looked playable, but the behavior felt inconsistent right away. The hint messages were backwards: when my guess was too high, it told me to go higher, and when it was too low, it told me to go lower. The attempt counter also started in a confusing state, so the displayed attempts left did not match what I expected on the first guess. I also noticed that the game sometimes compared guesses as strings on even attempts, which can create incorrect comparisons.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Copilot and ChatGPT while working through the bugs. A correct AI suggestion was to keep the secret number in Streamlit session state so it does not reset on reruns, and I verified that by checking the debug panel while submitting multiple guesses. Another helpful suggestion was to move pure game logic into a utility module and test it with pytest so behavior is easier to verify. A misleading suggestion I got was that the current hint logic was fine as long as emojis were clear, but manual testing proved the direction text was still wrong because "Too High" was paired with "Go HIGHER".

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I treated a bug as fixed only after both manual playtesting and automated tests agreed with expected behavior. I manually tested by opening the debug info, making guesses above and below the secret number, and confirming the hints matched the direction I should move. I also ran pytest, especially tests around check_guess, to verify that equal guesses return "Win", higher guesses return "Too High", and lower guesses return "Too Low". AI helped by suggesting edge cases to test, such as type mismatches and parsing unusual text input.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number kept changing because Streamlit reruns the script after each interaction, so values not stored in session state can be recreated. I would explain reruns as "the app script executes top to bottom every click," and session state as "the one place where values survive those reruns for one user session." Once I understood that model, the fix was to initialize the secret only when it does not already exist in session state. I also kept new-game behavior explicit so the secret only changes when the user intentionally starts over.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep is writing or running tests immediately after each small logic change instead of waiting until the end. Next time, I would ask AI for smaller, testable steps and demand expected input/output examples before applying suggestions. This project changed how I view AI-generated code: it is useful for speed, but it still needs careful human validation. I now treat AI output as a draft that must be debugged, tested, and reviewed like any other code.

---

## 6. AI Model Comparison (Challenge 5)

I compared a fix for the hint-direction bug using Copilot and ChatGPT. Copilot gave the more readable patch in this project because it matched my existing file structure and made small, targeted edits near the affected logic. ChatGPT gave a clearer explanation of *why* the bug happened (mismatch between outcome labels and feedback text), but its first suggestion was broader than needed for this codebase. I verified both suggestions by running pytest and manually testing in Streamlit with known high/low guesses from the debug panel.
