import streamlit as st
import random
from utils import update_score


def play():
    st.header("✊🖐️✌ Rock Paper Scissors")

    # --- Game setup ---
    choices = {
        "Rock": "✊",
        "Paper": "🖐️",
        "Scissors": "✌️"
    }

    # --- Layout buttons instead of selectbox ---
    st.subheader("Pick your move:")
    cols = st.columns(len(choices))
    player_choice = None
    for i, (move, emoji) in enumerate(choices.items()):
        if cols[i].button(f"{emoji} {move}"):
            player_choice = move

    # --- AI reacts only if player chose ---
    if player_choice:
        ai_choice = random.choice(list(choices.keys()))

        # Show what AI played
        st.markdown(f"🤖 AI plays: **{choices[ai_choice]} {ai_choice}**")

        # Decide outcome
        if player_choice == ai_choice:
            st.info("🤝 It's a draw!")
            update_score("draw", "Rock Paper Scissors", f"AI: {ai_choice}")
            st.caption("AI: *'Heh, we think alike 😏'*")
        elif (player_choice == "Rock" and ai_choice == "Scissors") or \
             (player_choice == "Paper" and ai_choice == "Rock") or \
             (player_choice == "Scissors" and ai_choice == "Paper"):
            st.success("✅ You win!")
            update_score("win", "Rock Paper Scissors", f"AI: {ai_choice}")
            st.caption("AI: *'Nooo! How did you know?! 😤'*")
        else:
            st.error("❌ You lose!")
            update_score("loss", "Rock Paper Scissors", f"AI: {ai_choice}")
            st.caption("AI: *'Haha! Too easy 😎'*")
