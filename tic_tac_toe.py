import streamlit as st
from utils import update_score

def play():
    st.header("❌⭕ Tic-Tac-Toe")

    if "board" not in st.session_state:
        st.session_state.board = [""] * 9
        st.session_state.turn = "X"

    def check_winner(board):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),
                (2,5,8),(0,4,8),(2,4,6)]
        for i,j,k in wins:
            if board[i] and board[i] == board[j] == board[k]:
                return board[i]
        return None

    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            idx = 3*i+j
            if cols[j].button(st.session_state.board[idx] or "-", key=f"ttt{idx}"):
                if not st.session_state.board[idx]:
                    st.session_state.board[idx] = st.session_state.turn
                    st.session_state.turn = "O" if st.session_state.turn == "X" else "X"

    winner = check_winner(st.session_state.board)
    if winner:
        st.success(f"🎉 Player {winner} wins!")
        update_score("win", "Tic Tac Toe", f"Winner: {winner}")
        st.session_state.board = [""] * 9
    elif all(st.session_state.board):
        st.info("🤝 It's a draw!")
        update_score("draw", "Tic Tac Toe", "Full board draw")
        st.session_state.board = [""] * 9
