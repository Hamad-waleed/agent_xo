import streamlit as st
import numpy as np
from TicTacToe3Pieces import TicTacToe3Pieces
from alpha_beta_Agent import alpha_beta
import time

st.set_page_config(page_title="AI Settings Mode", layout="centered")

# CSS لجعل اللوحة متلاصقة والتحكم بالواجهة
st.markdown("""
    <style>
    /* 1. تصفير الحاوية الكبيرة */
    .block-container {
        padding-top: 2rem !important;
    }

    /* 2. إلغاء أي مسافات عمودية بين العناصر */
    [data-testid="stVerticalBlock"] {
        gap: 0px !important;
    }
    
    /* 3. إلغاء الهوامش الداخلية لكل عنصر داخل الصفوف */
    [data-testid="stVerticalBlock"] > div {
        padding: 0px !important;
        margin: 0px !important;
    }

    /* 4. إلغاء الفراغات بين الأعمدة (المسافة الأفقية) */
    [data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
    }
    
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important;
        width: 300px !important;
        margin: auto !important;
    }

    /* 5. تصميم الأزرار - الحواف الحادة هي السر في التلاصق */
    .stButton > button {
        width: 100px !important;
        height: 100px !important;
        font-size: 40px !important;
        border: 1px solid #444 !important; /* خط نحيف جداً للشبكة */
        border-radius: 0px !important; /* زاوية حادة 100% */
        margin: 0px !important;
        padding: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)
# 1. لوحة التحكم في الجانب (Sidebar)
with st.sidebar:
    st.header("Settings")
    
    # اختيار مين يبدأ (مين الـ X)
    mode = st.radio("Who starts (as X)?", ("AI starts", "Human starts"))
    
    # التحكم بالديبث (من 1 إلى 9)
    chosen_depth = st.slider("AI Depth (Difficulty)", min_value=1, max_value=9, value=4)
    
    if st.button("Apply & Reset Game"):
        st.session_state.clear()
        st.rerun()

# 2. تهيئة اللعبة بناءً على الإعدادات
if 'game' not in st.session_state:
    st.session_state.game = TicTacToe3Pieces()
    st.session_state.ai = alpha_beta(depth=chosen_depth)
    
    if mode == "AI starts":
        st.session_state.player_val = -1 # Human is O
        st.session_state.ai_val = 1     # AI is X
        st.session_state.needs_ai_move = True
    else:
        st.session_state.player_val = 1  # Human is X
        st.session_state.ai_val = -1     # AI is O
        st.session_state.needs_ai_move = False

game = st.session_state.game
ai = st.session_state.ai

st.title("Custom AI Battle")
st.write(f"Mode: **{mode}** | Difficulty: **{chosen_depth}**")

# 3. منطق حركة الذكاء الاصطناعي
if st.session_state.get('needs_ai_move', False) and game.win_play(game.board) == 0:
    with st.spinner('AI is thinking...'):
        # تأخير للواقعية إلا في أول حركة باللعبة
        if np.sum(game.board != 0) > 0:
            time.sleep(1)
        
        # استدعاء الدالة المناسبة بناءً على هوية الـ AI (X أو O)
        if st.session_state.ai_val == 1:
            _, move = ai.all_alpha_beta_x(game.board, game, chosen_depth, -float('inf'), float('inf'), game.queu_x, game.queu_y)
        else:
            _, move = ai.all_alpha_beta_y(game.board, game, chosen_depth, -float('inf'), float('inf'), game.queu_x, game.queu_y)
            
        if move:
            target_q = game.queu_x if st.session_state.ai_val == 1 else game.queu_y
            game.make_move(game.board, move[0], move[1], st.session_state.ai_val, target_q)
            
    st.session_state.needs_ai_move = False
    st.rerun()

# 4. دالة ضغطة اللاعب
def handle_click(r, c):
    if game.board[r, c] == 0 and game.win_play(game.board) == 0:
        target_q = game.queu_x if st.session_state.player_val == 1 else game.queu_y
        game.make_move(game.board, r, c, st.session_state.player_val, target_q)
        st.session_state.needs_ai_move = True

# 5. رسم اللوحة
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        val = game.board[r, c]
        label = "X" if val == 1 else ("O" if val == -1 else " ")
        cols[c].button(label, key=f"cell-{r}-{c}", on_click=handle_click, args=(r, c))

# 6. النتائج
winner = game.win_play(game.board)
if winner != 0:
    if winner == st.session_state.ai_val:
        st.error("AI Wins! 🤖")
    else:
        st.success("You Win! 🎉")

if st.button("Quick Reset"):
    st.session_state.clear()
    st.rerun()