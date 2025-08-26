import streamlit as st
import random
from utils import update_score


def play():
    st.header("🔢 Number Guess Game (Player vs AI 🤖)")

    # --- Mode Selection ---
    mode = st.radio("Choose mode:", ["Solo", "Race vs AI"])

    # --- Difficulty ---
    difficulty = st.radio("Choose difficulty:", ["Easy (1-20)", "Medium (1-50)", "Hard (1-100)"])
    if difficulty.startswith("Easy"):
        max_num, max_attempts = 20, 6
    elif difficulty.startswith("Medium"):
        max_num, max_attempts = 50, 8
    else:
        max_num, max_attempts = 100, 10

    # --- AI Personality ---
    ai_personality = None
    if mode == "Race vs AI":
        ai_personality = st.radio("Choose AI personality:", ["🤪 Dumb", "🧠 Smart", "😈 Cheater"])

    # --- Init Session ---
    if "secret" not in st.session_state or st.session_state.get("reset", False):
        st.session_state.secret = random.randint(1, max_num)
        st.session_state.attempts = 0
        st.session_state.max_attempts = max_attempts
        st.session_state.reset = False
        st.session_state.ai_attempts = 0
        st.session_state.ai_guesses = set()
        st.session_state.ai_low = 1
        st.session_state.ai_high = max_num

    secret = st.session_state.secret

    # --- Player Guess ---
    guess = st.number_input(f"Your guess (1-{max_num})", min_value=1, max_value=max_num, step=1)

    if st.button("🎯 Submit Guess"):
        st.session_state.attempts += 1
        attempts_left = st.session_state.max_attempts - st.session_state.attempts

        # --- Check Player ---
        if guess == secret:
            st.success(f"🎉 You got it! The number was {secret}.")
            update_score("win", "Number Guess", f"Player guessed {guess} in {st.session_state.attempts} tries ({difficulty}, {mode})")
            st.session_state.reset = True

        else:
            diff = abs(guess - secret)
            if diff > max_num * 0.4:
                hint = "Way off!"
            elif diff > max_num * 0.2:
                hint = "Not close."
            else:
                hint = "🔥 Very close!"
            if guess < secret:
                st.warning(f"Too low! {hint} Attempts left: {attempts_left}")
                st.session_state.ai_low = max(st.session_state.ai_low, guess + 1)  # Smart AI update
            else:
                st.warning(f"Too high! {hint} Attempts left: {attempts_left}")
                st.session_state.ai_high = min(st.session_state.ai_high, guess - 1)  # Smart AI update

        # --- AI Turn (Race Mode) ---
        if mode == "Race vs AI" and not st.session_state.reset:
            st.session_state.ai_attempts += 1

            if ai_personality == "🤪 Dumb":
                ai_guess = random.randint(1, max_num)  # might repeat guesses

            elif ai_personality == "🧠 Smart":
                # binary search style guess
                ai_guess = (st.session_state.ai_low + st.session_state.ai_high) // 2

            elif ai_personality == "😈 Cheater":
                # Pretends to be dumb for 2 rounds, then guesses the secret
                if st.session_state.ai_attempts < 3:
                    ai_guess = random.randint(1, max_num)
                else:
                    ai_guess = secret

            # --- AI Feedback ---
            if ai_guess == secret:
                st.error(f"🤖 The {ai_personality} AI guessed {ai_guess} and WON!")
                update_score("loss", "Number Guess", f"AI ({ai_personality}) guessed {ai_guess} in {st.session_state.ai_attempts} tries ({difficulty}, {mode})")
                st.session_state.reset = True
            else:
                st.info(f"🤖 {ai_personality} AI guessed {ai_guess}... wrong!")

        # --- Game Over ---
        if not st.session_state.reset and st.session_state.attempts >= st.session_state.max_attempts:
            st.error(f"💀 Game Over! You ran out of tries. The number was {secret}.")
            update_score("loss", "Number Guess", f"Failed to guess ({difficulty}, {mode})")
            st.session_state.reset = True

    # --- Restart ---
    if st.button("🔄 Restart Game"):
        st.session_state.reset = True
        st.rerun()
