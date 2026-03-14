# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  Immediately noticed the "Developer Debug Info" section in the page. Upon clicking on it, I could see the "Secret", even before starting the game.
- List at least two concrete bugs you noticed at the start
  1."Show Hint" shows a glitching "Stop" sign at the top right corner before "Deploy" link for a breif second and disappears. The hints dont change with every answer submitted, even if the user needs       to go lower or higher it will keep on displaying "Go Higher" or "Go Lower" continuously.
  2. Attempts Left counter does not work. Hint
  3. Upon ending the game and winning, the game does not reset when "New Game" button is clicked but the details in "Developer Debug Info" changes. 
  

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  Claude 
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  Hardcoded display message instead of showing low-high based on the difficulty. Checked the code in app.py and it was hardcoded on line 110.
  Bug: f"Guess a number between 1 and 100. "  Fix: f"Guess a number between {low} and {high}. "
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  AI suggested the difficulty range would be: Easy 1-20, Normal 1-100 and Hard 1-200, but I did not suggest it. It is clear that the range should be 1-20, 1-50 and 1-100 based on the buggy code.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  After bug was fixed, relaunched the site and checked manually if it was really fixed. Created test cases to check if code passed the checks.
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  Mixed Inputs Test for the Guess Parser:
  This test verifies that parse_guess rejects input like "12abc". Something that starts as a number but contains non-numeric characters.
  def test_mixed_input(self):
        ok, val, err = parse_guess("12abc")
        assert ok is False
        assert err == "That is not a number."
- Did AI help you design or understand any tests? How?
  Yes AI helped me design and understand all the tests. I suggested some tests for the Guess Parser and it suggested other tests as well. It explained all the tests and why it was necessary. How? I wrote down specific instructions to explain all the logic in detail, why it was suggesting something, what was the impact, what it solved and how it solved it. 
  Example of above Parser test explanation from AI:
  Linebyline:                                                                                                                                                             1. parse_guess("12abc") — Passes the string "12abc" into the parser. Inside parse_guess, since there's no "." in the string, it tries int("12abc"), which raises a
   ValueError. The except Exception block catches it and returns (False, None, "That is not a number.").
  2. assert ok is False — Confirms the parse failed (first element of the returned tuple).
  3. assert err == "That is not a number." — Confirms the correct error message was returned (third element).

  Why it matters: Without this test, someone could accidentally make the parser more lenient (e.g., using a regex that grabs just the leading digits), which would  
  silently accept bad input. This ensures strict validation — the entire string must be a valid number.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Streamlit is a python framework that turns plain.py script into a web app. Every time a user interacts with a widget the entire app.py script re-executes from top to bottom. But that would mean all the interacted data like "Submitted Guess" or attempts would be lost. That is where the session state comes in. It is a persistent dictionary that survives across reruns. Reruns are the execution model, session state is the memory, and Streamlit handles turning Python into a live web app.

---

## 5. Looking ahead: your developer habits

-- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  I would like to implement a testing habit everyday, even for logic that I deemed not requiring any tests.
- What is one thing you would do differently next time you work with AI on a coding task?
  Use GIT differently. Commit for every small change with better explanations.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  Instructions to AI should be like writing a test case, check for every edge case. If something is not mentioned in the instructions, AI is fast to assume everything.
