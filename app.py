import streamlit as st
import numpy as np
from TicTacToe3Pieces import TicTacToe3Pieces
from alpha_beta_Agent import alpha_beta

# 1. Basic Setup
st.set_page_config(page_title="Tic Tac Toe AI", layout="centered")

if 'game' not in st.session_state:
    st.session_state.game = TicTacToe3Pieces()
    st.session_state.ai = alpha_beta(depth=1)
    # AI (X) makes the very first move of the game immediately
    score, move_x = st.session_state.ai.all_alpha_beta_x(
        st.session_state.game.board, st.session_state.game, 4, 
        -float('inf'), float('inf'), st.session_state.game.queu_x, st.session_state.game.queu_y
    )
    if move_x:
        st.session_state.game.make_move(st.session_state.game.board, move_x[0], move_x[1], 1, st.session_state.game.queu_x)

game = st.session_state.game
ai = st.session_state.ai

st.title("AI vs Human")
st.write("AI is **X** (Started first) | You are **O**")

# 2. Game Logic Function
def play_turn(r, c):
    if game.board[r, c] == 0:
        # Step 1: Your move (O)
        game.make_move(game.board, r, c, -1, game.queu_y)
        
        # Step 2: Check if you won
        if game.win_play(game.board) == 0:
            # Step 3: AI move (X)
            score, move_x = ai.all_alpha_beta_x(
                game.board, game, 4, -float('inf'), float('inf'), 
                game.queu_x, game.queu_y
            )
            if move_x:
                game.make_move(game.board, move_x[0], move_x[1], 1, game.queu_x)

# 3. Simple Grid UI
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        val = game.board[r, c]
        label = "X" if val == 1 else ("O" if val == -1 else " ")
        
        # Create the button
        cols[c].button(label, key=f"{r}-{c}", on_click=play_turn, args=(r, c))

# 4. Win Messages
winner = game.win_play(game.board)
if winner == 1:
    st.error("AI (X) Wins!")
elif winner == -1:
    st.success("You (O) Win!")

if st.button("Restart"):
    st.session_state.clear()
    st.rerun()