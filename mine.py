from TicTacToe3Pieces import TicTacToe3Pieces
from alpha_beta_Agent import alpha_beta
from MCTS import mcts
import time

game = TicTacToe3Pieces()
ai = alpha_beta(depth=12)

mc = mcts()




print("--- Game Started ---")
print("Initial Board:")
game.print_board()

# move = mc.search(game=game , bord = game.board , plyer=1 , que_x=game.queu_x , que_y=game.queu_y ,iter=100)
# move = ai.all_alpha_beta_x(game.board , game , 4 , -float('inf') , float('inf') , game.queu_x , game.queu_y)[1]
# print(f"the move is {move}")
# game.make_move(game.board , move[0] , move[1] , 1 , game.queu_x)

# game.print_board()

board = game.board
que_x = game.queu_x
que_y = game.queu_y

for i in range(15):

    print("the round is " , i+1)
    print("-"*20)
    x = mc.search(game , board , 1 , que_x , que_y ,1000)
    game.make_move(board , x[0] , x[1] , 1 , que_x)
    game.print_board()
    if(game.win_play(board)==1):
        print("X is win raond " , i+1)
        break
    


    o = ai.all_alpha_beta_y(board , game , 9 , -float('inf') , float('inf') , que_x , que_y)[1]
    game.make_move(board , o[0] , o[1] , -1 , que_y)
    game.print_board()
    if(game.win_play(board)== -1):
        print("O is win in raond " , i)
        break
    

    