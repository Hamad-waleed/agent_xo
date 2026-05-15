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

# mcts vs alpha beta and return avg time to move and result 
def mcts_vs_ab(game: TicTacToe3Pieces, ai :alpha_beta , mc :mcts , ai_depth=5, mc_iter=1000 ,match = 10):
    results = {"P1_Wins": 0, "P2_Wins": 0 , 'Draws' :0}
    time_P1 = []
    time_P2 = []

    for zzz in range(match):
        game.reset_game()
        board = game.board
        que_x = game.queu_x
        que_y = game.queu_y

        i = 0
        while(game.win_play(board)==0):
            if(i >25):
                results['Draws'] +=1
                break
            print("the round is " , i+1)
            print("-"*20)

            start = time.time()
            x = mc.search(game , board , 1 , que_x , que_y ,mc_iter)
            end = time.time()

            time_P1.append(end-start)

            game.make_move(board , x[0] , x[1] , 1 , que_x)
            game.print_board()
            if(game.win_play(board)==1):
                print("X is win raond " , i+1)
                results['P1_Wins'] +=1
                break
            

            start = time.time()
            o = ai.all_alpha_beta_y(board , game , ai_depth, -float('inf') , float('inf') , que_x , que_y)[1]
            end = time.time()

            time_P2.append(end-start)

            game.make_move(board , o[0] , o[1] , -1 , que_y)
            game.print_board()
            if(game.win_play(board)== -1):
                print("O is win in raond " , i)
                results['P2_Wins'] +=1
                break
            i +=1
            
    avg_P1 = sum(time_P1)/len(time_P1)
    avg_P2 = sum(time_P2)/len(time_P2)


    return {
        "results": results,
        "avg_mcts_time_ms": avg_P1*1000,
        "avg_ab_time_ms": avg_P2*1000,
        "total time to one match S" : avg_P1*i+avg_P2*i,
        "one move x , o ms" :(time_P1[0]*1000, time_P2[0]*1000)
    } 

# alpha beta vs alpha beta and return avg time to move and result 
def ab_vs_ab(game: TicTacToe3Pieces, ai :alpha_beta , depth_x=5 , depth_o=5 , match = 10):
    results = {"P1_Wins": 0, "P2_Wins": 0 , 'Draws' :0}
    time_P1 = []
    time_P2 = []

    for zzz in range(match):
        game.reset_game()
        board = game.board
        que_x = game.queu_x
        que_y = game.queu_y

        i = 0
        while(game.win_play(board)==0):
            if(i >25):
                results['Draws'] +=1
                break

            print("the round is " , i+1)
            print("-"*20)

            #  X player
            start = time.time()
            x = ai.all_alpha_beta_x(board , game , depth_x , -float('inf') , float('inf') , que_x , que_y)[1]
            end = time.time()

            time_P1.append(end-start)

            game.make_move(board , x[0] , x[1] , 1 , que_x)
            game.print_board()
            if(game.win_play(board)==1):
                print("X is win raond " , i+1)
                results['P1_Wins'] +=1
                break
        
            # O player
            start = time.time()
            o = ai.all_alpha_beta_y(board , game , depth_o, -float('inf') , float('inf') , que_x , que_y)[1]
            end = time.time()

            time_P2.append(end-start)

            game.make_move(board , o[0] , o[1] , -1 , que_y)
            game.print_board()
            if(game.win_play(board)== -1):
                print("O is win in raond " , i)
                results['P2_Wins'] +=1
                break
            i +=1
            
    avg_P1 = sum(time_P1)/len(time_P1)
    avg_P2 = sum(time_P2)/len(time_P2)


    return {
        "results": results,
        "avg_ap_X_time_ms": avg_P1*1000,
        "avg_ab_O_time_ms": avg_P2*1000,
        "total time to one match S" : avg_P1*i+avg_P2*i,
        "one move xo MS" :(time_P1[0]*1000 , time_P2[0]*1000)
    } 

def mctc_vs_mcts(game , mc , iter_x=100, iter_o=100, match = 10):
    results = {"P1_Wins": 0, "P2_Wins": 0 , 'Draws' :0}
    time_P1 = []
    time_P2 = []

    for zzz in range(match):
        game.reset_game()
        board = game.board
        que_x = game.queu_x
        que_y = game.queu_y

        i = 0
        while(game.win_play(board)==0):
            if(i >25):
                results['Draws'] +=1
                break

            print("the round is " , i+1)
            print("-"*20)

            start = time.time()
            x = mc.search(game , board , 1 , que_x , que_y ,iter_x)
            end = time.time()

            time_P1.append(end-start)

            

            game.make_move(board , x[0] , x[1] , 1 , que_x)
            game.print_board()
            if(game.win_play(board)==1):
                print("X is win raond " , i+1)
                results['P1_Wins'] +=1
                break
            

            start = time.time()
            o = mc.search(game , board , -1 , que_x , que_y ,iter_o)
            end = time.time()

            time_P2.append(end-start)

            game.make_move(board , o[0] , o[1] , -1 , que_y)
            game.print_board()
            if(game.win_play(board)== -1):
                print("O is win in raond " , i)
                results['P2_Wins'] +=1
                break
            i +=1
            
    avg_P1 = sum(time_P1)/len(time_P1)
    avg_P2 = sum(time_P2)/len(time_P2)


    return {
        "results": results,
        "avg_ap_X_time_ms": avg_P1*1000,
        "avg_ab_O_time_ms": avg_P2*1000,
        "total time to one match S" : avg_P1*i+avg_P2*i,
        "one move xo MS" :(time_P1[0]*1000, time_P2[0]*1000)
    }



test =mcts_vs_ab(game , ai ,mc,6 , 1000 ,50)

# test = ab_vs_ab(game , ai ,5,5)

# test = mctc_vs_mcts(game , mc ,10 ,10,10)

print(test)