from gmpy2 import xmpz


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
            print("i+j (" + str(j) + " " + str(i) + " )" + str(game[i * 6 + j]))
            # print(board[i][j])
            if game[i * 6 + j] == 0:
                board[j][i] = 1
            else:
               board[j][i] = 2
            # print(board[j][i])
    return board

def heurastic():
    return score
# game[0:3] = 7|game[42:62]
game = xmpz(0)
# game[0:63]=~0
# game=game.bit_clear(42)
# game=game.bit_clear(45)
# game=game.bit_clear(48)
# game=game.bit_clear(51)
# game=game.bit_clear(54)
# game=game.bit_clear(57)
# game=game.bit_clear(60)
print((game[42:63]))
# # game[45:48]=~0
# print(bin(game))
# print(game.bit_length())
state, game = play(0, game, 1)
state, game = play(0, game, 1)
state, game = play(0, game, 1)
state, game = play(0, game, 1)
state, game = play(0, game, 1)
state, game = play(0, game, 1)
# print(game,state)
state, game = play(1, game, 1)
state, game = play(1, game, 1)
state, game = play(1, game, 1)
state, game = play(1, game, 1)
state, game = play(1, game, 1)
state, game = play(1, game, 1)
state, game = play(1, game, 1)
# print(state)
state, game = play(2, game, 1)
state, game = play(2, game, 1)
state, game = play(2, game, 1)
state, game = play(2, game, 1)
state, game = play(2, game, 1)
state, game = play(2, game, 1)
state, game = play(2, game, 1)
# print(state)
state, game = play(3, game, 1)
state, game = play(3, game, 1)
state, game = play(3, game, 1)
state, game = play(3, game, 1)
state, game = play(3, game, 1)
state, game = play(3, game, 1)
state, game = play(3, game, 1)
state, game = play(4, game, 1)
state, game = play(4, game, 1)
state, game = play(4, game, 1)
state, game = play(4, game, 1)
state, game = play(4, game, 1)
state, game = play(4, game, 0)
# state,game= play(4,game,0)
state, game = play(5, game, 1)
state, game = play(5, game, 1)
state, game = play(5, game, 1)
state, game = play(5, game, 1)
state, game = play(5, game, 1)
state, game = play(5, game, 1)
state, game = play(5, game, 1)
state, game = play(6, game, 1)
state, game = play(6, game, 1)
state, game = play(6, game, 1)
state, game = play(6, game, 1)
state, game = play(6, game, 1)
state, game = play(6, game, 1)
state, game = play(6, game, 1)
state, game = play(6, game, 1)
data = bit_to_matrix(game=game)
# print(bit_to_matrix(game=xmpz(0)))
for row in data:
    print(row)
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
    # board = bit_to_matrix(board)
    player1_sc=0
    player2_sc=0
    for i in range(0,6):
        for j in range(0,7):
            if board[i][j]==0:
                """
                in the end of game it must all places are full 
                """
                return None
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
board = [
    [1,2,2,2,2,1,2],
    [1,2,1,1,1,1,2],
    [1,1,2,1,2,2,1],
    [1,1,1,2,1,2,2],
    [1,2,1,2,1,1,2],
    [1,1,1,1,1,1,2],
]
a,b=calculate_final_score(board)
print(a,b)
