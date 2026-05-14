import copy

class alpha_beta:
    def __init__(self , depth):
        self.depth = depth



    def all_alpha_beta_x(self , board ,game , depth , alpha ,beta , q_x , q_y):
        
        if depth == 0 or game.win_play(board) != 0:
            return game.evaluate(board, q_x, q_y), None
        
        all_move = game.genret_move(board)
        best_move = None
        max_evale = -float('inf')


        for i in all_move:
            temp_board = copy.deepcopy(board)
            temp_qx = copy.deepcopy(q_x)
            temp_qy = copy.deepcopy(q_y)

            game.make_move(temp_board , i[0]  , i[1], 1 , temp_qx )
            score ,_ =self.all_alpha_beta_y(temp_board , game , depth-1 , alpha , beta , temp_qx , temp_qy)
            if score > max_evale:
                max_evale = score
                best_move = i

            alpha = max(alpha, score)
            if beta <= alpha: # التقليم اهم شي 
                break
        
        return max_evale , best_move
    
    def all_alpha_beta_y(self , board ,game , depth , alpha ,beta , q_x , q_y):
        if depth == 0 or game.win_play(board) != 0:
            return game.evaluate(board, q_x, q_y), None
        
        all_move = game.genret_move(board)
        best_move = None
        min_evale = float('inf')

        for i in all_move:
            temp_board = copy.deepcopy(board)
            temp_qx = copy.deepcopy(q_x)
            temp_qy = copy.deepcopy(q_y)

            game.make_move(temp_board , i[0]  , i[1], -1 , temp_qy)
            score , _ = self.all_alpha_beta_x(temp_board , game , depth-1 , alpha , beta , temp_qx , temp_qy)

            if score < min_evale:
                min_evale = score
                best_move = i
            beta = min(score , beta)
            if beta <= alpha:
                break
        

        return min_evale ,best_move