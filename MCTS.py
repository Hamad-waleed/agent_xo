import copy
import math
import random
from collections import deque
class mcts_node:
    def __init__(self , board , parent=None, move=None, player=1, que_x=None, que_o=None):
        self.board = copy.deepcopy(board)
        self.parent = parent
        self.move = move
        self.player = player
        self.que_x = copy.deepcopy(que_x) if que_x else deque()
        self.que_o = copy.deepcopy(que_o) if que_o else deque()


        self.children = []    # الأغصان اللي طالعة من هذه العقدة
        self.wins = 0         # عدد مرات الفوز (W)
        self.visits = 0       # عدد مرات الزيارة (N)
        self.untried_moves = None


class mcts:
    def __init__(self):
        pass

    # نختار افضل ولد واذا فيه ولد ما مريناه نختاره
    def Selection(self , node:mcts_node):
        child = node.children
        best_cild = None
        max_ucb = -float('inf')

        for i in child:
            if i.visits == 0:
                return i
            # UCB1
            exploitation = i.wins / i.visits
            exploration = 1.41 * math.sqrt(math.log(node.visits) / i.visits)
            ucb_value = exploitation + exploration

            if (ucb_value > max_ucb):
                max_ucb = ucb_value
                best_cild = i
               
        return best_cild
    
    #  يعني تغتح غصن جديد , نحركة بحركة وحدة  
    def Expansion(self , node:mcts_node , game ):

        move = node.untried_moves.pop()

        temp_pord = copy.deepcopy(node.board)
        q_x = copy.deepcopy(node.que_x)
        q_y = copy.deepcopy(node.que_o)

        current_q = q_x if node.player == 1 else q_y
        game.make_move(temp_pord , move[0] , move[1] , node.player , current_q)

        new_chiled = mcts_node(temp_pord, node , move ,-node.player , q_x , q_y )
        node.children.append(new_chiled)    
        return new_chiled

    # نحاكي لين ناصل فوز او خسارة او تعادل 50 جولة 
    def Simulation(self ,node :mcts_node, game):
        countre = 0
        temp_board = copy.deepcopy(node.board)
        q_x = copy.deepcopy(node.que_x)
        q_y = copy.deepcopy(node.que_o)
        pl = node.player
        # check to win 
        winner = game.win_play(temp_board)
        if winner != 0:
            return winner
        
        # 50 round  XO 
        while(countre <= 50):
            all_move = game.genret_move(temp_board)
            move = random.choice(all_move)

            current_q = q_x if pl == 1 else q_y
            game.make_move(temp_board , move[0] ,move[1] ,pl , current_q)

            winer = game.win_play(temp_board) 
            if winer == 1 or winer == -1: return winer

            countre +=1
            pl = -pl
        return winer
            
    # نحسب الغصن كم مره جيناه وكم مره فاز
    def Backpropagation(self , node:mcts_node , winner):
        current = node
        while current is not None:
            current.visits += 1
            if current.parent is not None:
                if current.parent.player == winner:
                    current.wins += 1
                elif winner == 0:
                    current.wins += 0.5
            current = current.parent

# نجمع كل الي قبل
    def search(self , game , board , plyer , que_x , que_y , iter = 1000):

        root = mcts_node(board=board  , player=plyer , que_x=que_x , que_o = que_y)

        root.untried_moves = game.genret_move(board)

        for i in range(iter):
            node  = root 

            # --- PHASE 1: Selection ---
            while not node.untried_moves and node.children:
                node = self.Selection(node)
            
            # --- PHASE 2: Expansion ---
            # إذا العقدة عندها حركات لسا ما جربناها، نفتح غصن جديد
            if node.untried_moves:
                node = self.Expansion(node, game)
                node.untried_moves = game.genret_move(node.board)

            # --- PHASE 3: Simulation ---
            winner = self.Simulation(node, game)

            # --- PHASE 4: Backpropagation ---
            self.Backpropagation(node, winner)
        # القرار النهائي
        best_move_node = max(root.children, key=lambda c: c.visits)
        return best_move_node.move