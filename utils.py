import json, os
import streamlit as st

HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_score(result, game_name, details=""):
    player = st.session_state.player_name
    all_data = load_history()

    if result == "win":
        st.session_state.scoreboard["wins"] += 1
        outcome = "✅ Win"
    elif result == "loss":
        st.session_state.scoreboard["losses"] += 1
        outcome = "❌ Loss"
    elif result == "draw":
        st.session_state.scoreboard["draws"] += 1
        outcome = "🤝 Draw"
    else:
        outcome = "❓ Unknown"

    st.session_state.history.append({
        "game": game_name,
        "outcome": outcome,
        "details": details
    })

    # Save back to JSON
    all_data[player] = {
        "scoreboard": st.session_state.scoreboard,
        "history": st.session_state.history
    }
    save_history(all_data)
