import streamlit as st
from utils import load_history, save_history
import tic_tac_toe
import number_guess
import rock_paper_scissors

st.set_page_config(page_title="Mini Arcade", page_icon="🎮", layout="centered")

# ---- SESSION STATE INIT ----
if "player_name" not in st.session_state:
    st.session_state.player_name = None
if "scoreboard" not in st.session_state:
    st.session_state.scoreboard = {"wins": 0, "losses": 0, "draws": 0}
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🎮 Mini Arcade")
st.subheader("Welcome to the Mini Arcade!")

# ---- PLAYER LOGIN ----
player_name = st.text_input("Enter your player name:")

if player_name:
    all_data = load_history()
    if player_name not in all_data:
        all_data[player_name] = {
            "scoreboard": {"wins": 0, "losses": 0, "draws": 0},
            "history": []
        }
        save_history(all_data)

    st.session_state.player_name = player_name
    st.session_state.scoreboard = all_data[player_name]["scoreboard"]
    st.session_state.history = all_data[player_name]["history"]

    st.success(f"👋 Hello, {player_name}! Choose a game to play.")

    # ---- GAME SELECTOR ----
    game_choice = st.selectbox("Choose a game:", 
        ["Tic-Tac-Toe", "Number Guess", "Rock Paper Scissors"])

    if game_choice == "Tic-Tac-Toe":
        tic_tac_toe.play()
    elif game_choice == "Number Guess":
        number_guess.play()
    elif game_choice == "Rock Paper Scissors":
        rock_paper_scissors.play()

    # ---- SHOW SCOREBOARD ----
    st.markdown("## 🏆 Scoreboard")
    st.write(st.session_state.scoreboard)

    # ---- SHOW HISTORY ----
    st.markdown("## 📜 Game History")
    for h in st.session_state.history[-10:][::-1]:  # show last 10
        st.write(f"🎲 {h['game']} → {h['outcome']} ({h['details']})")

    # ---- RESET BUTTON ----
    if st.button("🔄 Reset My History"):
        st.session_state.scoreboard = {"wins": 0, "losses": 0, "draws": 0}
        st.session_state.history = []
        all_data = load_history()
        all_data[st.session_state.player_name] = {
            "scoreboard": st.session_state.scoreboard,
            "history": st.session_state.history
        }
        save_history(all_data)
        st.success("Your history has been reset!")
