import gmpy2
from gmpy2 import xmpz
FOUR_CONNECTED =  [4000,-4500]
THREE_CONNECTED = [500,-500]
TWO_CONNECTED = [100,-100]
UN_CONNECTED=[500,-590]
EMPTY = [50,-50]
UNEMPTY = [-20,20]

# from 0 to 41 is our board
# from 42 to 63 each three bits represent column [6,7]
def play(col, game=xmpz(0), player=0):
    """
    this function take current game state and
    the player who have the turn 0 for player 1 and 2 for player 2
    and column in which place he wanna to play in it 
    then return new game state and true if valid play and false if play not valid
    """
    if checkEnd(game):
        return False, game
    if col >= 7:
        return False, game
    elif col < 0:
        return False, game
    start_index = 42 + col * 3
    end_index = start_index + 3
    if game[start_index:end_index] == 6:
        return False, game
    elif game[start_index:end_index] < 6:
        required_bit = col * 6 + game[start_index:end_index]
        if player == 0:
            game = game.bit_clear(required_bit)
            # print(game)
        else:
            game = game.bit_set(required_bit)
            # print(game)
        req_sum = xmpz(0)
        req_sum = req_sum.bit_set(start_index)
        # print(bin(req_sum))
        # print("GGGGG "+bin(req_sum + game))
        game = req_sum + game
        # print("start "+str(start_index)+" en "+str(end_index))
        return True, game
    return False, game


def checkEnd(game):
    """
    this function take game state and check if it the last state of game 
    by make sure all column are complete it will be complete if bits = 110 110 110 110 110 110 110
    """
    if (game[42:63] == 1797558):
        return True
    else:
        return False
def bit_to_matrix(game):
    """
    this function take game as bits and return 2D array
    it will by used in gui and heuristic
    """
    board = [[0 for i in range(7)] for j in range(6)]
    # print(board)
    board[0][0]=2
    for i in range(0, 7):
        start_index = 42 + i * 3
        end_index = start_index + 3
        last_row = game[start_index:end_index]
        # print(last_row)
        last_row = last_row.numerator
        a = 0|last_row
        for j in range(0, last_row):
            # print("i+j (" + str(j) + " " + str(i) + " )" + str(game[i * 6 + j]))
            # print(board[i][j])
            if game[i * 6 + j] == 0:
                board[j][i] = 1
            else:
               board[j][i] = 2
            # print(board[j][i])
    return board
def max_horiz(game,i,j,visited):
    if j==6:
        visited[i][j][0]=True
        return 1
    if j+1>6:
        return 0
    if game[i][j]!=game[i][j+1]:
        visited[i][j][0]=True
        return 1
    if game[i][j]==game[i][j+1]:
        visited[i][j][0]=True
        return max_horiz(game,i,j+1,visited)+1
def max_vert(game,i,j,visited):
    if i==5:
        visited[i][j][1]=True
        return 1
    if i+1>5:
        return 0
    if game[i][j]!=game[i+1][j]:
        visited[i][j][1]=True
        return 1
    if game[i][j]==game[i+1][j]:
        visited[i][j][1]=True
        return max_vert(game,i+1,j,visited)+1
def max_p_d(game,i,j,visited):
    if j==6 or i==5:
        visited[i][j][2]=True
        return 1
    if j+1>6 or i+1>5:
        return 0
    if game[i][j]!=game[i+1][j+1]:
        visited[i][j][2]=True
        return 1
    if game[i][j]==game[i+1][j+1]:
        visited[i][j][2]=True
        return max_p_d(game,i+1,j+1,visited)+1
def max_n_d(game,i,j,visited):
    if j==0 or i==5:
        visited[i][j][3]=True
        return 1
    if j-1<0 or i+1>5:
        return 0
    if game[i][j]!=game[i+1][j-1]:
        visited[i][j][3]=True
        return 1
    if game[i][j]==game[i+1][j-1]:
        visited[i][j][3]=True
        return max_p_d(game,i+1,j-1,visited)+1
def un_connected_weighted_horz(board,i,j,visited,max_before,score):
    if j+max_before<7 and board[i][j]!=board[i][j+max_before] and board[i][j+max_before]!=0:
        if max_before!=1:
            score+=(max_before/7)*UNEMPTY[board[i][j]-1]
    else:
        k= j+max_before
        mx_h=max_before
        while k<7 and  board[i][k]==0:
            if(mx_h!=1):
                score+=(mx_h/7)*EMPTY[board[i][j]-1]
            if k+1>=7 or board[i][j]!=board[i][k+1]:
                break
            if k+1<7 and board[i][j]==board[i][k+1]:
                mx_h=max_horiz(board,i,k+1,visited)
                if mx_h == 1:
                    if board[i][j]==1:
                        score+=5
                    else:
                        score-=10
                elif mx_h==2:
                    score+=TWO_CONNECTED[board[i][j]-1]
                    score+=UN_CONNECTED[board[i][j]-1]*(1/4.0)
                elif mx_h==3:
                    score+=THREE_CONNECTED[board[i][j]-1]
                    score+=UN_CONNECTED[board[i][j]-1]*(2/4.0)
                elif mx_h==4:
                    score+=FOUR_CONNECTED[board[i][j]-1]
                    score+=UN_CONNECTED[board[i][j]-1]*(3/4.0)
                k=k+mx_h+1
            if k<7 and board[i][k]!=board[i][j] and board[i][k]!=0:
                if mx_h!=1:
                    score+=(mx_h/7)*UNEMPTY[board[i][j]-1]
    return score
def un_connected_d_p(board,i,j,visited,max_before,score):
    if i+max_before<6 and j+max_before<7 and board[i][j]!=board[i+max_before][j] and board[i+max_before][j+max_before]!=0:
        if max_before!=1:
            score+=(max_before/6)*UNEMPTY[board[i][j]-1]
    else:
        new_i= i+max_before
        new_j= j+max_before
        mx_h=max_before
        while new_i<6 and new_j<7 and  board[new_i][new_j]==0:
            if mx_h!=1:
                score+=(mx_h/6)*EMPTY[board[i][j]-1]
            if new_i+1>=6 or new_j+1>=7 or board[i][j]!=board[new_i+1][new_j+1]:
                break
            if new_i+1<6 and new_j+1<7 and board[i][j]==board[new_i+1][new_j+1]:
                mx_h=max_p_d(board,new_i+1,new_j+1,visited)
                if mx_h == 1:
                    if board[i][j]==1:
                        score+=5
                    else:
                        score-=10
                elif mx_h==2:
                    score+=TWO_CONNECTED[board[i][j]-1]
                    score+=UN_CONNECTED[board[i][j]-1]*(1/4.0)
                elif mx_h==3:
                    score+=THREE_CONNECTED[board[i][j]-1]
                    score+=UN_CONNECTED[board[i][j]-1]*(2/4.0)
                elif mx_h==4:
                    score+=FOUR_CONNECTED[board[i][j]-1]
                    score+=UN_CONNECTED[board[i][j]-1]*(3/4.0)
                new_i=new_i+mx_h+1
                new_j=new_j+mx_h+1
            if new_i<6 and new_j<7 and board[new_i][new_j]!=board[i][j] and board[new_i][new_j]!=0 :
                if(mx_h!=1):
                    score+=(mx_h/6)*UNEMPTY[board[i][j]-1]
    return score
def un_connected_d_n(board,i,j,visited,max_before,score):
    if i+max_before<6 and j-max_before>-1 and board[i][j]!=board[i+max_before][j-max_before] and board[i+max_before][j-max_before]!=0:
        if max_before!=1:
            score+=(max_before/6)*UNEMPTY[board[i][j]-1]
    else:
        new_i= i+max_before
        new_j= j-max_before
        mx_h=max_before
        while new_i<6 and new_j>-1 and  board[new_i][new_j]==0:
            if mx_h!=1:
                score+=(mx_h/6)*EMPTY[board[i][j]-1]
            if new_i+1>=6 or new_j-1<0 or board[i][j]!=board[new_i+1][new_j-1]:
                break
            if new_i+1<6 and new_j-1>-1 and board[i][j]==board[new_i+1][new_j-1]:
                mx_h=max_n_d(board,new_i+1,new_j-1,visited)
                if mx_h == 1:
                    if board[i][j]==1:
                        score+=5
                    else:
                        score-=10
                elif mx_h==2:
                    score+=TWO_CONNECTED[board[i][j]-1]
                    score+=UN_CONNECTED[board[i][j]-1]*(1/4.0)
                elif mx_h==3:
                    score+=THREE_CONNECTED[board[i][j]-1]
                    score+=UN_CONNECTED[board[i][j]-1]*(2/4.0)
                elif mx_h==4:
                    score+=FOUR_CONNECTED[board[i][j]-1]
                    score+=UN_CONNECTED[board[i][j]-1]*(3/4.0)
                # k=k+mx_h+1
                new_i=new_i+mx_h+1
                new_j=new_j-mx_h-1
            if new_i<6 and new_j>-1 and board[new_i][new_j]!=board[i][j] and board[new_i][new_j]!=0 :
                if mx_h!=1:
                    score+=(mx_h/6)*UNEMPTY[board[i][j]-1]
    return score
def heurastic1(game):
    board=bit_to_matrix(game)
    """
    visited is 3d array to reduce reduandancy
    every intial element responsible for direct 0 horiz 1 ver 2 postive diagonal 
    3 negative diagonal
    """
    visited= [[[False for k in range(4)] for j in range(7)] for i in range(6)] 
    score=0
    for i in range(0,6):
        for j in range(0,7):
            if board[i][j]==0:
                continue
            if(not visited[i][j][0]):
                mx=max_horiz(board,i,j,visited)
                if mx>=4:
                    score+=FOUR_CONNECTED[board[i][j]-1]*(mx-3)
                    k= j+mx
                    if k<7:
                        if board[k][j]==0:
                            score+=EMPTY[board[i][j]-1]
                        if k+1<7 and board[i][j]==board[i][k+1]:
                            max_h=max_horiz(board,i,k+1,visited)
                            if max_h==2:
                                score+=TWO_CONNECTED[board[i][j]-1]
                                score+=UN_CONNECTED[board[i][j]-1]*(1/4.0)
                            if max_h==1:
                                if board[i][j]==1:
                                    score+=5
                                else:
                                    score-=10
                elif mx==3:
                    score+=THREE_CONNECTED[board[i][j]-1]
                    score=un_connected_weighted_horz(board,i,j,visited,mx,score)
                elif mx==2:
                    score+=TWO_CONNECTED[board[i][j]-1]
                    score=un_connected_weighted_horz(board,i,j,visited,mx,score)
                elif mx==1:
                    score=un_connected_weighted_horz(board,i,j,visited,mx,score)
            if(not visited[i][j][1]):
                max=max_vert(board,i,j,visited)
                if max>=4:
                    score+=FOUR_CONNECTED[board[i][j]-1]*(max-3)
                elif max==3:
                    score+=THREE_CONNECTED[board[i][j]-1]
                    if i+max<6 and board[i][j]!=board[i+max][j] and board[i+max][j]!=0:
                        score+=UNEMPTY[board[i][j]-1]
                elif max==2:
                    score+=TWO_CONNECTED[board[i][j]-1]
            if(not visited[i][j][2]):
                max=max_p_d(board,i,j,visited)
                if max>=4:
                    score+=FOUR_CONNECTED[board[i][j]-1]*(max-3)
                    new_i= i+max
                    new_j=j+max
                    if new_i<6 and new_j<7 and board[new_i][new_j]==0:
                        score+=EMPTY[board[i][j]-1]
                        if max==4:
                            if new_i+1<6 and new_j+1<7 and board[i][j]==board[new_i+1][new_j+1]:
                                if board[i][j]==1:
                                    score+=5
                                else:
                                    score-=10 
                elif max==3:
                    score+=THREE_CONNECTED[board[i][j]-1]
                    score=un_connected_d_p(board,i,j,visited,max,score)
                elif max==2:
                    score+=TWO_CONNECTED[board[i][j]-1]
                    score=un_connected_d_p(board,i,j,visited,max,score)
                elif max==1:
                    score=un_connected_d_p(board,i,j,visited,max,score)
            if(not visited[i][j][3]):
                max=max_n_d(board,i,j,visited)
                if max>=4:
                    score+=FOUR_CONNECTED[board[i][j]-1]*(max-3)
                    new_i= i+max
                    new_j=j-max
                    if new_i<6 and new_j>-1 and board[new_i][new_j]==0:
                        score+=EMPTY[board[i][j]-1]
                        if max==4:
                            if new_i+1<6 and new_j+1<7 and board[i][j]==board[new_i+1][new_j+1]:
                                if board[i][j]==1:
                                    score+=5
                                else:
                                    score-=10 
                elif max==3:
                    score+=THREE_CONNECTED[board[i][j]-1]
                    score=un_connected_d_n(board,i,j,visited,max,score)
                elif max==2:
                    score+=TWO_CONNECTED[board[i][j]-1]
                    score=un_connected_d_n(board,i,j,visited,max,score)
                elif max==1:
                    score=un_connected_d_n(board,i,j,visited,max,score)
    PRIORITY=3
    for i in range(0,2):
        for j in range(0,7):
            if board[i][j]==1:
                score+=PRIORITY
            elif board[i][j]==2:
                score-=PRIORITY
    for i in range(0,6):
        for j in range(0,3):
            if board[i][j]==1:
                score+=PRIORITY
            elif board[i][j]==2:
                score-=PRIORITY
    return score
def four_horz(board,i,j):
    if board[i][j]==board[i][j+1] and board[i][j]==board[i][j+2] and board[i][j]==board[i][j+3]:
        return 1 
    else:
        return 0
def four_vert(board,i,j):
    if board[i][j]==board[i+1][j] and board[i][j]==board[i+2][j] and board[i][j]==board[i+3][j]:
        return 1 
    else:
        return 0
def four_diagonally_ne(board,i,j):
    if board[i][j]==board[i+1][j+1] and board[i][j]==board[i+2][j+2] and board[i][j]==board[i+3][j+3]:
        return 1 
    else:
        return 0
def four_diagonally_nw(board,i,j):
    if board[i][j]==board[i+1][j-1] and board[i][j]==board[i+2][j-2] and board[i][j]==board[i+3][j-3]:
        return 1 
    else:
        return 0
def calculate_final_score(board):
    board = bit_to_matrix(board)
    player1_sc=0
    player2_sc=0
    for i in range(0,6):
        for j in range(0,7):
            if board[i][j]==0:
                """
                in the end of game it must all places are full 
                """
                continue
            if board[i][j]==1:
                if i+3<6:
                    player1_sc+=four_vert(board,i,j)
                    if j+3<7:
                        player1_sc+=four_diagonally_ne(board,i,j)
                    if j-3>=0:
                        player1_sc+=four_diagonally_nw(board,i,j)
                if j+3<7:
                    player1_sc+=four_horz(board,i,j)
            elif board[i][j]==2:
                if i+3<6:
                    player2_sc+=four_vert(board,i,j)
                    if j+3<7:
                        player2_sc+=four_diagonally_ne(board,i,j)
                    if j-3>=0:
                        player2_sc+=four_diagonally_nw(board,i,j)
                if j+3<7:
                    player2_sc+=four_horz(board,i,j)
    return player1_sc,player2_sc
    