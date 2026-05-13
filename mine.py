from TicTacToe3Pieces import TicTacToe3Pieces
from alpha_beta_Agent import alpha_beta
import time

game = TicTacToe3Pieces()
ai = alpha_beta(depth=12)

# تنفيذ حركات لتجربة حذف القطع
# game.make_move(game.board, 1, 1, 1, game.queu_x)
# game.make_move(game.board, 0, 0, 1, game.queu_x)
# game.make_move(game.board, 2, 2, 1, game.queu_x)
# # الحركة الرابعة ستحذف أول قطعة (1,1)
# game.make_move(game.board, 0, 1, 1, game.queu_x)


print("--- Game Started ---")
print("Initial Board:")
print(game.board)

for turn in range(1, 11):
    print(f"\n--- Round {turn} ---")
    
    # 1. Player X Turn (Maximizer)
    print("Player X is thinking...")
    score_x, move_x = ai.all_alpha_beta_x(
        game.board, game, ai.depth, -float('inf'), float('inf'), game.queu_x, game.queu_y
    )
    
    if move_x:
        game.make_move(game.board, move_x[0], move_x[1], 1, game.queu_x)
        print(f"Player X chose: {move_x}")
    
    print(game.board)
    
    # Check if X won
    if game.win_play(game.board) == 1:
        print("\nGAME OVER! Winner is: Player X (1)")
        break

    # 2. Player O Turn (Minimizer)
    print("\nPlayer O is thinking...")
    score_o, move_o = ai.all_alpha_beta_y(
        game.board, game, ai.depth, -float('inf'), float('inf'), game.queu_x, game.queu_y
    )
    
    if move_o:
        game.make_move(game.board, move_o[0], move_o[1], -1, game.queu_y)
        print(f"Player O chose: {move_o}")
    
    print(game.board)

    # Check if O won
    if game.win_play(game.board) == -1:
        print("\nGAME OVER! Winner is: Player O (-1)")
        break
    
    time.sleep(1)