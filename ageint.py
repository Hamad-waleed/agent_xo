import numpy as np 
from collections import deque
game = np.zeros((3,3), dtype=int)


queu_x = deque()
queu_y = deque()

# print(game)


# to genrat the all posipal move
def genret_move(bord):
    expexted = []
    # row
    for row in range(3):
        # columan
        for columan in range(3):
            if bord[row , columan] == 0:
                expexted.append((row,columan))
    return expexted
# print(genret_move(game))

def win_play(bord):
    num = 0
    # this to win in the row
    for row in range(3):
        temp = bord[row , :].sum()
        if( temp ==3 or temp ==-3 ): 
            num = temp
            break
    # this to win in coulman
    for columan in range(3):
        temp = bord[: , columan].sum()
        if( temp ==3 or temp ==-3 ): 
            num = temp
            break

    # digonal
    temp = bord[0,0]+bord[1,1]+bord[2,2]
    if( temp ==3 or temp ==-3 ): 
            num = temp
    temp = bord[0,2]+bord[1,1]+bord[2,0]
    if( temp ==3 or temp ==-3 ): 
            num = temp
     
    if(num>0):
        return 1
    elif(num<0):
        return -1
    else:
        return 0


def make_move(bord , row :int, coulman :int , player :int , player_que :deque):
    if win_play(bord) != 0:
        return False

    if(len(player_que) == 3):
        old_r , old_c = player_que.popleft()
        bord[old_r , old_c] = 0
    if(bord[row ,coulman] != 0):
         return False
    bord[row ,coulman] = player
    
    player_que.append((row , coulman))
    return True

make_move(game , 1,2,1,queu_x)
make_move(game , 2,2,1,queu_x)
make_move(game , 1,1,1,queu_x)
make_move(game , 2,0,1,queu_x)

# اذا كان فيه اكسين جمب بعض ترجع عشرهتاخذ هل البحث بالصفوف او الاعمدة او الاقطار وتخاذ رقم العامود او الصف
def help_evaluate(bord , way , ind , player):
    scoor = 0
    # rows
    if way ==0:
        elements, counts = np.unique(bord[ind , :], return_counts=True)
        frequencies = dict(zip(elements, counts))
        if  frequencies.get(player ,0) == 2:scoor = 10
        return scoor
#   columan
    elif way == 1:
        elements, counts = np.unique(bord[: , ind], return_counts=True)
        frequencies = dict(zip(elements, counts))
        if  frequencies.get(player ,0) == 2:scoor = 10
        return scoor
    # digonal
    elif way == 2:
        temp1 = bord[0,0]+bord[1,1]+bord[2,2]
        temp2 =bord[0,2]+bord[1,1]+bord[2,0]
        if temp1 == 2:scoor += 10
        if temp2 == 2:scoor += 10
        return scoor
    else:
        return False
        




def evaluate(bord , que_x ,que_y):
    winner = win_play(bord)
    if winner ==1 :return 100 , 0
    if winner ==-1 :return 0,-100

    score_x = 0
    for i in range(3):
        for x in range(3):
            score_x= score_x+help_evaluate(bord , i , x , 1)
            if i ==2:
                break

    score_y = 0
    for i in range(3):
        for x in range(3):
            score_y = score_y + help_evaluate(bord , i , x , -1)
            if i == 2:
                break

    return score_x,score_y



game[1,1] = 1
game[2,2] = 0
game[1,2] = 1

print(game)
print(evaluate(game , queu_x , queu_y))



