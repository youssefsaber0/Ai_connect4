from BitOperations import bits_to_matrix

FOUR_CONNECTED = [4000, -4500]
THREE_CONNECTED = [500, -500]
TWO_CONNECTED = [100, -100]
UN_CONNECTED = [500, -590]
EMPTY = [50, -50]
NONEMPTY = [-20, 20]


def heuristic_one(state):
    board = bits_to_matrix(state)
    """
    visited is 3d array to reduce reduandancy
    every intial element responsible for direct 0 horiz 1 ver 2 postive diagonal 
    3 negative diagonal
    """
    visited = [[[False for k in range(4)] for j in range(7)] for i in range(6)]
    score = 0
    for i in range(0, 6):
        for j in range(0, 7):
            if board[i][j] == 0:
                continue
            if not visited[i][j][0]:
                mx = max_horiz(board, i, j, visited)
                if mx >= 4:
                    score += FOUR_CONNECTED[board[i][j] - 1] * (mx - 3)
                    k = j + mx
                    if k < 7:
                        if board[k][j] == 0:
                            score += EMPTY[board[i][j] - 1]
                        if k + 1 < 7 and board[i][j] == board[i][k + 1]:
                            max_h = max_horiz(board, i, k + 1, visited)
                            if max_h == 2:
                                score += TWO_CONNECTED[board[i][j] - 1]
                                score += UN_CONNECTED[board[i][j] - 1] * (1 / 4.0)
                            if max_h == 1:
                                if board[i][j] == 1:
                                    score += 5
                                else:
                                    score -= 10
                elif mx == 3:
                    score += THREE_CONNECTED[board[i][j] - 1]
                    score = un_connected_weighted_horz(board, i, j, visited, mx, score)
                elif mx == 2:
                    score += TWO_CONNECTED[board[i][j] - 1]
                    score = un_connected_weighted_horz(board, i, j, visited, mx, score)
                elif mx == 1:
                    score = un_connected_weighted_horz(board, i, j, visited, mx, score)
            if not visited[i][j][1]:
                max = max_vert(board, i, j, visited)
                if max >= 4:
                    score += FOUR_CONNECTED[board[i][j] - 1] * (max - 3)
                elif max == 3:
                    score += THREE_CONNECTED[board[i][j] - 1]
                    if i + max < 6 and board[i][j] != board[i + max][j] and board[i + max][j] != 0:
                        score += NONEMPTY[board[i][j] - 1]
                elif max == 2:
                    score += TWO_CONNECTED[board[i][j] - 1]
            if not visited[i][j][2]:
                max = max_p_d(board, i, j, visited)
                if max >= 4:
                    score += FOUR_CONNECTED[board[i][j] - 1] * (max - 3)
                    new_i = i + max
                    new_j = j + max
                    if new_i < 6 and new_j < 7 and board[new_i][new_j] == 0:
                        score += EMPTY[board[i][j] - 1]
                        if max == 4:
                            if new_i + 1 < 6 and new_j + 1 < 7 and board[i][j] == board[new_i + 1][new_j + 1]:
                                if board[i][j] == 1:
                                    score += 5
                                else:
                                    score -= 10
                elif max == 3:
                    score += THREE_CONNECTED[board[i][j] - 1]
                    score = un_connected_d_p(board, i, j, visited, max, score)
                elif max == 2:
                    score += TWO_CONNECTED[board[i][j] - 1]
                    score = un_connected_d_p(board, i, j, visited, max, score)
                elif max == 1:
                    score = un_connected_d_p(board, i, j, visited, max, score)
            if not visited[i][j][3]:
                max = max_n_d(board, i, j, visited)
                if max >= 4:
                    score += FOUR_CONNECTED[board[i][j] - 1] * (max - 3)
                    new_i = i + max
                    new_j = j - max
                    if new_i < 6 and new_j > -1 and board[new_i][new_j] == 0:
                        score += EMPTY[board[i][j] - 1]
                        if max == 4:
                            if new_i + 1 < 6 and new_j + 1 < 7 and board[i][j] == board[new_i + 1][new_j + 1]:
                                if board[i][j] == 1:
                                    score += 5
                                else:
                                    score -= 10
                elif max == 3:
                    score += THREE_CONNECTED[board[i][j] - 1]
                    score = un_connected_d_n(board, i, j, visited, max, score)
                elif max == 2:
                    score += TWO_CONNECTED[board[i][j] - 1]
                    score = un_connected_d_n(board, i, j, visited, max, score)
                elif max == 1:
                    score = un_connected_d_n(board, i, j, visited, max, score)
    PRIORITY = 3
    for i in range(0, 2):
        for j in range(0, 7):
            if board[i][j] == 1:
                score += PRIORITY
            elif board[i][j] == 2:
                score -= PRIORITY
    for i in range(0, 6):
        for j in range(0, 3):
            if board[i][j] == 1:
                score += PRIORITY
            elif board[i][j] == 2:
                score -= PRIORITY
    return score


def max_horiz(game, i, j, visited):
    if j == 6:
        visited[i][j][0] = True
        return 1
    if j + 1 > 6:
        return 0
    if game[i][j] != game[i][j + 1]:
        visited[i][j][0] = True
        return 1
    if game[i][j] == game[i][j + 1]:
        visited[i][j][0] = True
        return max_horiz(game, i, j + 1, visited) + 1


def max_vert(game, i, j, visited):
    if i == 5:
        visited[i][j][1] = True
        return 1
    if i + 1 > 5:
        return 0
    if game[i][j] != game[i + 1][j]:
        visited[i][j][1] = True
        return 1
    if game[i][j] == game[i + 1][j]:
        visited[i][j][1] = True
        return max_vert(game, i + 1, j, visited) + 1


def max_p_d(game, i, j, visited):
    if j == 6 or i == 5:
        visited[i][j][2] = True
        return 1
    if j + 1 > 6 or i + 1 > 5:
        return 0
    if game[i][j] != game[i + 1][j + 1]:
        visited[i][j][2] = True
        return 1
    if game[i][j] == game[i + 1][j + 1]:
        visited[i][j][2] = True
        return max_p_d(game, i + 1, j + 1, visited) + 1


def max_n_d(game, i, j, visited):
    if j == 0 or i == 5:
        visited[i][j][3] = True
        return 1
    if j - 1 < 0 or i + 1 > 5:
        return 0
    if game[i][j] != game[i + 1][j - 1]:
        visited[i][j][3] = True
        return 1
    if game[i][j] == game[i + 1][j - 1]:
        visited[i][j][3] = True
        return max_p_d(game, i + 1, j - 1, visited) + 1


def un_connected_weighted_horz(board, i, j, visited, max_before, score):
    if j + max_before < 7 and board[i][j] != board[i][j + max_before] and board[i][j + max_before] != 0:
        if max_before != 1:
            score += (max_before / 7) * NONEMPTY[board[i][j] - 1]
    else:
        k = j + max_before
        mx_h = max_before
        while k < 7 and board[i][k] == 0:
            if mx_h != 1:
                score += (mx_h / 7) * EMPTY[board[i][j] - 1]
            if k + 1 >= 7 or board[i][j] != board[i][k + 1]:
                break
            if k + 1 < 7 and board[i][j] == board[i][k + 1]:
                mx_h = max_horiz(board, i, k + 1, visited)
                if mx_h == 1:
                    if board[i][j] == 1:
                        score += 5
                    else:
                        score -= 10
                elif mx_h == 2:
                    score += TWO_CONNECTED[board[i][j] - 1]
                    score += UN_CONNECTED[board[i][j] - 1] * (1 / 4.0)
                elif mx_h == 3:
                    score += THREE_CONNECTED[board[i][j] - 1]
                    score += UN_CONNECTED[board[i][j] - 1] * (2 / 4.0)
                elif mx_h == 4:
                    score += FOUR_CONNECTED[board[i][j] - 1]
                    score += UN_CONNECTED[board[i][j] - 1] * (3 / 4.0)
                k = k + mx_h + 1
            if k < 7 and board[i][k] != board[i][j] and board[i][k] != 0:
                if mx_h != 1:
                    score += (mx_h / 7) * NONEMPTY[board[i][j] - 1]
    return score


def un_connected_d_p(board, i, j, visited, max_before, score):
    if i + max_before < 6 and j + max_before < 7 and board[i][j] != board[i + max_before][j] and board[i + max_before][
        j + max_before] != 0:
        if max_before != 1:
            score += (max_before / 6) * NONEMPTY[board[i][j] - 1]
    else:
        new_i = i + max_before
        new_j = j + max_before
        mx_h = max_before
        while new_i < 6 and new_j < 7 and board[new_i][new_j] == 0:
            if mx_h != 1:
                score += (mx_h / 6) * EMPTY[board[i][j] - 1]
            if new_i + 1 >= 6 or new_j + 1 >= 7 or board[i][j] != board[new_i + 1][new_j + 1]:
                break
            if new_i + 1 < 6 and new_j + 1 < 7 and board[i][j] == board[new_i + 1][new_j + 1]:
                mx_h = max_p_d(board, new_i + 1, new_j + 1, visited)
                if mx_h == 1:
                    if board[i][j] == 1:
                        score += 5
                    else:
                        score -= 10
                elif mx_h == 2:
                    score += TWO_CONNECTED[board[i][j] - 1]
                    score += UN_CONNECTED[board[i][j] - 1] * (1 / 4.0)
                elif mx_h == 3:
                    score += THREE_CONNECTED[board[i][j] - 1]
                    score += UN_CONNECTED[board[i][j] - 1] * (2 / 4.0)
                elif mx_h == 4:
                    score += FOUR_CONNECTED[board[i][j] - 1]
                    score += UN_CONNECTED[board[i][j] - 1] * (3 / 4.0)
                new_i = new_i + mx_h + 1
                new_j = new_j + mx_h + 1
            if new_i < 6 and new_j < 7 and board[new_i][new_j] != board[i][j] and board[new_i][new_j] != 0:
                if (mx_h != 1):
                    score += (mx_h / 6) * NONEMPTY[board[i][j] - 1]
    return score


def un_connected_d_n(board, i, j, visited, max_before, score):
    if i + max_before < 6 and j - max_before > -1 and board[i][j] != board[i + max_before][j - max_before] and \
            board[i + max_before][j - max_before] != 0:
        if max_before != 1:
            score += (max_before / 6) * NONEMPTY[board[i][j] - 1]
    else:
        new_i = i + max_before
        new_j = j - max_before
        mx_h = max_before
        while new_i < 6 and new_j > -1 and board[new_i][new_j] == 0:
            if mx_h != 1:
                score += (mx_h / 6) * EMPTY[board[i][j] - 1]
            if new_i + 1 >= 6 or new_j - 1 < 0 or board[i][j] != board[new_i + 1][new_j - 1]:
                break
            if new_i + 1 < 6 and new_j - 1 > -1 and board[i][j] == board[new_i + 1][new_j - 1]:
                mx_h = max_n_d(board, new_i + 1, new_j - 1, visited)
                if mx_h == 1:
                    if board[i][j] == 1:
                        score += 5
                    else:
                        score -= 10
                elif mx_h == 2:
                    score += TWO_CONNECTED[board[i][j] - 1]
                    score += UN_CONNECTED[board[i][j] - 1] * (1 / 4.0)
                elif mx_h == 3:
                    score += THREE_CONNECTED[board[i][j] - 1]
                    score += UN_CONNECTED[board[i][j] - 1] * (2 / 4.0)
                elif mx_h == 4:
                    score += FOUR_CONNECTED[board[i][j] - 1]
                    score += UN_CONNECTED[board[i][j] - 1] * (3 / 4.0)
                # k=k+mx_h+1
                new_i = new_i + mx_h + 1
                new_j = new_j - mx_h - 1
            if new_i < 6 and new_j > -1 and board[new_i][new_j] != board[i][j] and board[new_i][new_j] != 0:
                if mx_h != 1:
                    score += (mx_h / 6) * NONEMPTY[board[i][j] - 1]
    return score


def heuristic_two(state):
    board = bits_to_matrix(state)
    player1_sc = 0
    player2_sc = 0
    for i in range(0, 6):
        for j in range(0, 7):
            score = 0
            if board[i][j] == 0:
                continue
            #################################################################################################
            n = n_vert(board, i, j)
            barr = 0
            if i + n < 6 and board[i + n][j] == 0:
                barr = 1
            score += getscore(n, 0, 0, barr, 0)
            #################################################################################################
            n = n_diagonally_ne(board, i, j)
            opens, barr, barr2, n2 = 0, 0, 0, 0
            if i + n < 6 and j + n < 7 and board[i + n][j + n] == 0 and not (
                    n < 4 and i - 1 >= 0 and j - 1 >= 0 and board[i - 1][j - 1] == board[i][j]):
                opens += 1
            if opens > 0:
                barr += n_diagonally_ne(board, i + n, j + n)
                for q in range(barr):
                    if board[i + n + q - 1][j + n + q] != 0:
                        barr2 += 1
            if i + n + barr < 6 and j + n + barr < 7 and board[i + n + barr][j + n + barr] == board[i][j]:
                n2 = n_diagonally_ne(board, i + n + barr, j + n + barr)
            barr2 = barr + barr2
            prev = 0
            while i - prev >= 0 and j - prev >= 0 and board[i - prev][j - prev] == 0:
                prev = prev + 1
            score += getscore(n, n2, barr2 - 1, barr, prev)
            #################################################################################################
            n = n_diagonally_nw(board, i, j)
            opens, barr, barr2, n2 = 0, 0, 0, 0
            if i + n < 6 and j - n >= 0 and board[i + n][j - n] == 0 and not (
                    n < 4 and i - 1 >= 0 and j + 1 < 7 and board[i - 1][j + 1] == board[i][j]):
                opens += 1
            if opens > 0:
                barr += n_diagonally_nw(board, i + n, j - n)
                for q in range(barr):
                    if board[i + n + q - 1][j - n - q] != 0:
                        barr2 += 1
            if i + n + barr < 6 and j - n - barr >= 0 and board[i + n + barr][j - n - barr] == board[i][j]:
                n2 = n_diagonally_nw(board, i + n + barr, j - n - barr)
            barr2 = barr + barr2
            prev = 0
            while i - prev >= 0 and j + prev < 7 and board[i - prev][j + prev] == 0:
                prev = prev + 1
            score += getscore(n, n2, barr2 - 1, barr, prev)
            #################################################################################################
            n = n_horz(board, i, j)
            opens, barr, barr2, n2 = 0, 0, 0, 0
            if j + n < 7 and board[i][j + n] == 0 and not (n < 4 and j - 1 >= 0 and board[i][j - 1] == board[i][j]):
                opens += 1
            if opens > 0:
                barr += n_horz(board, i, j + n)
                for q in range(barr):
                    if i - 1 < 0 or board[i - 1][j + n + q] != 0:
                        barr2 += 1
            if j + n + barr < 7 and board[i][j + n + barr] == board[i][j]:
                n2 = n_horz(board, i, j + n + barr)
            barr2 = barr + barr2
            prev = 0
            while j - prev - 1 >= 0 and board[i][j - prev - 1] == 0:
                prev = prev + 1
            score += getscore(n, n2, barr2 - 1, barr, prev)
            #################################################################################################
            if board[i][j] == 1:
                player1_sc += score
            else:
                player2_sc += score

    return player1_sc - player2_sc


def n_horz(board, i, j):
    n = 1
    while j + n < 7 and board[i][j] == board[i][j + n]:
        n = n + 1
    return n


def n_vert(board, i, j):
    n = 1
    while i + n < 6 and board[i][j] == board[i + n][j]:
        n = n + 1
    return n


def n_diagonally_ne(board, i, j):
    n = 1
    while i + n < 6 and j + n < 7 and board[i][j] == board[i + n][j + n]:
        n = n + 1
    return n


def n_diagonally_nw(board, i, j):
    n = 1
    while i + n < 6 and j - n >= 0 and board[i][j] == board[i + n][j - n]:
        n = n + 1
    return n


def getscore(n, n2, barr2, nextzeros, prevzeros):
    if barr2 < 0:
        barr2 = 0
    score = 0
    if n >= 4:
        score += 250
    if n >= 3:
        new = n2 + nextzeros - barr2
    elif n == 2:
        new = n2 + nextzeros - barr2 - 1
    elif n == 1:
        new = n2 + nextzeros - barr2 - 2
    if new < 0:
        new = 0
    score += 50 * new
    score += (nextzeros + prevzeros) * 7;
    return score
