import numpy as np 
from collections import deque
import copy
class TicTacToe3Pieces:
    def __init__(self):
        self.board = np.zeros((3,3), dtype=int)
        self.queu_x = deque()
        self.queu_y = deque()


# to genrat the all posipal move
    def genret_move(self,board):
        expexted = []
        # row
        for row in range(3):
            # columan
            for columan in range(3):
                if board[row , columan] == 0:
                    expexted.append((row,columan))
        return expexted
# print(genret_move(board))

    def win_play(self,board):
        num = 0
        # this to win in the row
        for row in range(3):
            temp = board[row , :].sum()
            if( temp ==3 or temp ==-3 ): 
                num = temp
                break
        # this to win in coulman
        for columan in range(3):
            temp = board[: , columan].sum()
            if( temp ==3 or temp ==-3 ): 
                num = temp
                break
        # digonal
        temp = board[0,0]+board[1,1]+board[2,2]
        if( temp ==3 or temp ==-3 ): 
                num = temp
        temp = board[0,2]+board[1,1]+board[2,0]
        if( temp ==3 or temp ==-3 ): 
                num = temp
        
        if(num>0):
            return 1
        elif(num<0):
            return -1
        else:
            return 0


    def make_move(self ,  board , row :int, coulman :int , player :int , player_que :deque):
        if self.win_play(board) != 0:
            return False

        if(len(player_que) == 3):
            old_r , old_c = player_que.popleft()
            board[old_r , old_c] = 0
        if(board[row ,coulman] != 0):
            return False
        board[row ,coulman] = player
        
        player_que.append((row , coulman))
        return True

    def reset_game(self):
    
        self.board = np.zeros((3,3), dtype=int)
        self.queu_x = deque()
        self.queu_y = deque()
          
        return self.board
    
    
    def cliening_eva(self, board , que_x , que_y):
        temp_board = copy.deepcopy(board)

        if len(que_x )== 3:
            r_x, c_x = que_x[0]
            temp_board[r_x , c_x] = 0
        if len (que_y)==3:
            r_y, c_y = que_y[0]
            temp_board[r_y , c_y] = 0

        return temp_board

    def evaluate(self , board , que_x , que_y):
        winner = self.win_play(board)
        if winner ==1 :return 1000
        if winner ==-1 :return -1000
        score = 0
        board = self.cliening_eva(board , que_x ,que_y)
        # دالة داخلية صغيرة لفحص الخطوط (صفوف، أعمدة، أقطار)
        def check_line(line, player):
            elements, counts = np.unique(line, return_counts=True)
            freq = dict(zip(elements, counts))
            # إذا وجدنا قطعتين للاعب والخانة الثالثة فارغة (تهديد حقيقي)
            if freq.get(player, 0) == 2 and freq.get(0, 0) == 1:
                return 20
            return 0
        
        for i in range(3):
            score += check_line(board[i, :], 1)   
            score -= check_line(board[i, :], -1)  
            score += check_line(board[:, i], 1)   
            score -= check_line(board[:, i], -1) 
        
        # فحص الاقطار  
        diag1 = np.diag(board)
        diag2 = np.diag(np.fliplr(board))
        score += check_line(diag1, 1) + check_line(diag2, 1)
        score -= check_line(diag1, -1) + check_line(diag2, -1)
        return score

    def print_board(self):
        print("\n-------------")
        for row in self.board:
            print("|", end=" ")
            for cell in row:
                if cell == 1:
                    char = 'X'
                elif cell == -1:
                    char = 'O'
                else:
                    char = ' ' # أو حط '.' إذا تبي الفراغ يبين
                print(f"{char} |", end=" ")
            print("\n-------------")




