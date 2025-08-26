import streamlit as st
from utils import update_score
import math
import random

def play():
    st.header("❌⭕ Tic-Tac-Toe")

    if "board" not in st.session_state:
        st.session_state.board = [""] * 9
        st.session_state.turn = "X"
    if "last_click" not in st.session_state:
        st.session_state.last_click = None

    def check_winner(board):
        wins = [(0,1,2),(3,4,5),(6,7,8),
                (0,3,6),(1,4,7),(2,5,8),
                (0,4,8),(2,4,6)]
        for i,j,k in wins:
            if board[i] and board[i] == board[j] == board[k]:
                return board[i]
        return None

    def available_moves(board):
        return [i for i, spot in enumerate(board) if spot == ""]

    # --- Minimax AI for "O" ---
    def minimax(board, depth, is_maximizing):
        winner = check_winner(board)
        if winner == "X": return -1
        if winner == "O": return 1
        if not available_moves(board): return 0

        if is_maximizing:
            best_score = -math.inf
            for move in available_moves(board):
                board[move] = "O"
                score = minimax(board, depth+1, False)
                board[move] = ""
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for move in available_moves(board):
                board[move] = "X"
                score = minimax(board, depth+1, True)
                board[move] = ""
                best_score = min(score, best_score)
            return best_score

    def ai_move(board, difficulty):
        if difficulty == "Easy":
            return random.choice(available_moves(board))
        else:
            best_score = -math.inf
            best_move = None
            for move in available_moves(board):
                board[move] = "O"
                score = minimax(board, 0, False)
                board[move] = ""
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_move if best_move is not None else random.choice(available_moves(board))

    # --- Draw board (buttons) ---
    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            idx = 3*i+j
            if cols[j].button(st.session_state.board[idx] or "-", key=f"ttt{idx}"):
                st.session_state.last_click = idx  # record the move

    # --- Process the click AFTER UI draw ---
    if st.session_state.last_click is not None:
        idx = st.session_state.last_click
        if not st.session_state.board[idx] and not check_winner(st.session_state.board):
            st.session_state.board[idx] = st.session_state.turn
            st.session_state.turn = "O" if st.session_state.turn == "X" else "X"

            # AI plays right after player move
            if mode == "Vs AI" and st.session_state.turn == "O" and not check_winner(st.session_state.board):
                ai_idx = ai_move(st.session_state.board, difficulty)
                st.session_state.board[ai_idx] = "O"
                st.session_state.turn = "X"

        st.session_state.last_click = None  # reset click

    # --- Check game state ---
    winner = check_winner(st.session_state.board)
    if winner:
        st.success(f"🎉 Player {winner} wins!")
        if mode == "2 Players":
            outcome = "win"
        else:
            outcome = "win" if winner == "X" else "loss"
        update_score(outcome, "Tic Tac Toe", f"Winner: {winner} ({mode}, {difficulty if difficulty else 'N/A'})")
        st.session_state.board = [""] * 9
    elif all(st.session_state.board):
        st.info("🤝 It's a draw!")
        update_score("draw", "Tic Tac Toe", f"Full board draw ({mode}, {difficulty if difficulty else 'N/A'})")
        st.session_state.board = [""] * 9
