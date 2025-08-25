import streamlit as st
import random
from utils import update_score

def play():
    st.header("🔢 Number Guess Game")

    if "secret" not in st.session_state:
        st.session_state.secret = random.randint(1, 20)

    guess = st.number_input("Guess a number (1-20)", min_value=1, max_value=20, step=1)

    if st.button("Submit Guess"):
        if guess == st.session_state.secret:
            st.success("🎉 Correct! You win!")
            update_score("win", "Number Guess", f"Guessed {guess}")
            st.session_state.secret = random.randint(1, 20)
        elif guess < st.session_state.secret:
            st.warning("Too low! Try again.")
        else:
            st.warning("Too high! Try again.")
