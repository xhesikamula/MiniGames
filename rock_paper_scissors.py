import streamlit as st
import random
from utils import update_score

def play():
    st.header("✊🖐️✌ Rock Paper Scissors")
#change the design
    choices = ["Rock", "Paper", "Scissors"]
    player_choice = st.selectbox("Choose your move:", choices)
    if st.button("Play!"):
        ai_choice = random.choice(choices)
        st.write(f"🤖 AI chose: {ai_choice}")

        if player_choice == ai_choice:
            st.info("🤝 It's a draw!")
            update_score("draw", "Rock Paper Scissors", f"AI: {ai_choice}")
        elif (player_choice == "Rock" and ai_choice == "Scissors") or \
             (player_choice == "Paper" and ai_choice == "Rock") or \
             (player_choice == "Scissors" and ai_choice == "Paper"):
            st.success("✅ You win!")
            update_score("win", "Rock Paper Scissors", f"AI: {ai_choice}")
        else:
            st.error("❌ You lose!")
            update_score("loss", "Rock Paper Scissors", f"AI: {ai_choice}")
