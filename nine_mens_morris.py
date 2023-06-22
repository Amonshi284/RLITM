from ned import nmm_place

board = [[0 for x in range(8)] for y in range(3)]


class Player:
    def __init__(self, token):
        self.token = token
        if self.token == "X":
            self.name = "\033[0;37;41mPlayer 1\033[0m"
        if self.token == "O":
            self.name = "\033[0;37;44mPlayer 2\033[0m"

    def current_player_tokens(self):
        token_count = 0
        for x in range(3):
            for y in range(8):
                if board[x][y] == self.token:
                    token_count += 1
        return token_count

    def has_legal_moves(self):
        for x in range(3):
            for y in range(8):
                if board[x][y] == self.token:
                    if get_legal_moves(x, y) != "":
                        return True
        return False


class BotPlayer(Player):
    def __init__(self, token):
        super().__init__(token)
        self.token = token
        if self.token == "X":
            self.name = "\033[0;37;41mPlayer 1\033[0m"
        if self.token == "O":
            self.name = "\033[0;37;44mPlayer 2\033[0m"

    def move(self):
        nmm_place(1)


player1 = Player("X")
player2 = BotPlayer("O")


def print_board():
    # ╔ ═ ╦ ╗ ║ ╠ ╬ ╣ ╚ ╩ ╝
    string = ""
    string += board[0][0].__str__() + "\t═\t═\t═\t═\t═\t" + board[0][1].__str__() + "\t═\t═\t═\t═\t═\t" + board[0][
        2].__str__() + "\n"
    string += "║\t\t\t\t\t\t║\t\t\t\t\t\t║" + "\n"
    string += "║\t\t" + board[1][0].__str__() + "\t═\t═\t═\t" + board[1][1].__str__() + "\t═\t═\t═\t" + board[1][
        2].__str__() + "\t\t║" + "\n"
    string += "║\t\t║\t\t\t\t║\t\t\t\t║\t\t║" + "\n"
    string += "║\t\t║\t\t" + board[2][0].__str__() + "\t═\t" + board[2][1].__str__() + "\t═\t" + board[2][
        2].__str__() + "\t\t║\t\t║" + "\n"
    string += "║\t\t║\t\t║\t\t\t\t║\t\t║\t\t║" + "\n"
    string += board[0][7].__str__() + "\t═\t" + board[1][7].__str__() + "\t═\t" + board[2][7].__str__() + "\t\t\t\t" + \
              board[2][3].__str__() + "\t═\t" + board[1][3].__str__() + "\t═\t" + board[0][3].__str__() + "\n"
    string += "║\t\t║\t\t║\t\t\t\t║\t\t║\t\t║" + "\n"
    string += "║\t\t║\t\t" + board[2][6].__str__() + "\t═\t" + board[2][5].__str__() + "\t═\t" + board[2][
        4].__str__() + "\t\t║\t\t║" + "\n"
    string += "║\t\t║\t\t\t\t║\t\t\t\t║\t\t║" + "\n"
    string += "║\t\t" + board[1][6].__str__() + "\t═\t═\t═\t" + board[1][5].__str__() + "\t═\t═\t═\t" + board[1][
        4].__str__() + "\t\t║" + "\n"
    string += "║\t\t\t\t\t\t║\t\t\t\t\t\t║" + "\n"
    string += board[0][6].__str__() + "\t═\t═\t═\t═\t═\t" + board[0][5].__str__() + "\t═\t═\t═\t═\t═\t" + board[0][
        4].__str__() + "\n"
    string = string.replace("0", "╬")
    string = string.replace("X", "\033[0;37;41mX\033[0m")
    string = string.replace("O", "\033[0;37;44mO\033[0m")
    string += "\n" + player1.name + " Current Tokens: " + player1.current_player_tokens().__str__() + " \t" + player2.name + " Current Tokens: " + player2.current_player_tokens().__str__()
    print(string)


def input_and_validation(player):
    valid = 0
    while valid == 0:
        x = int(input(player.name + " Outside = 0, Center = 1, Inside = 2\n"))
        while x > 2 or x < 0:
            print("incorrect input")
            x = int(input(player.name + " Outside = 0, Center = 1, Inside = 2\n"))
        y = int(input("0 - 7 Clockwise\n"))
        while y > 7 or y < 0:
            print("incorrect input")
            y = int(input("0 - 7 Clockwise\n"))
        if board[x][y] != 0 and board[x][y] != "╬":
            print("Position besetzt, neue Eingabe " + board[x][y].__str__())
        else:
            board[x][y] = player.token
            if token_check(x, y):
                print("Mühle :D")
                print_board()
                remove_token(player)
            valid = 1


def check():
    for x in range(3):
        for y in range(0, 7, 2):
            if y > 4:
                if board[x][y + 0] == board[x][y + 1] == board[x][0] and board[x][y + 0] != 0:
                    return True
            elif board[x][y + 0] == board[x][y + 1] == board[x][y + 2] and board[x][y + 0] != 0:
                return True
    for y in range(0, 7, 2):
        if board[0][y + 1] == board[1][y + 1] == board[2][y + 1] and board[0][y + 0] != 0:
            return True
    return False


def token_check(x, y):
    if y == 0 or y == 6 or y == 7:
        if board[x][0] == board[x][7] == board[x][6]:
            return True
    if y % 2 == 0:
        if y != 0:
            if board[x][y] == board[x][y - 1] == board[x][y - 2]:
                return True
        if y != 6:
            if board[x][y] == board[x][y + 1] == board[x][y + 2]:
                return True
    if y % 2 == 1 and y != 7:
        if board[x][y] == board[x][y + 1] == board[x][y - 1]:
            return True
        if board[0][y] == board[1][y] == board[2][y]:
            return True
    return False


def free_token_exits():
    for x in range(3):
        for y in range(8):
            if not token_check(x, y):
                return True
    return False


def get_legal_moves(x, y):
    legal_moves = ""
    if y == 0:
        if board[x][7] == 0:
            legal_moves += x.__str__() + "7 "
        if board[x][1] == 0:
            legal_moves += x.__str__() + "1"
        return legal_moves
    if y == 7:
        if board[x][6] == 0:
            legal_moves += x.__str__() + "6 "
        if board[x][0] == 0:
            legal_moves += x.__str__() + "0"
        if x != 2:
            if board[x + 1][y] == 0:
                legal_moves += " " + (x + 1).__str__() + y.__str__()
        if x != 0:
            if board[x - 1][y] == 0:
                legal_moves += " " + (x - 1).__str__() + y.__str__()
        return legal_moves
    if board[x][y - 1] == 0:
        legal_moves += x.__str__() + (y - 1).__str__() + " "
    if board[x][y + 1] == 0:
        legal_moves += x.__str__() + (y + 1).__str__() + " "
    if y % 2 != 0:
        if x != 2:
            if board[x + 1][y] == 0:
                legal_moves += (x + 1).__str__() + y.__str__() + " "
        if x != 0:
            if board[x - 1][y] == 0:
                legal_moves += (x - 1).__str__() + y.__str__()
        return legal_moves
    return legal_moves


def move_token(player, x, y):
    legal_moves = get_legal_moves(x, y)
    print(legal_moves)
    valid_input = False
    while not valid_input:
        x = int(input(player.name + " Outside = 0, Center = 1, Inside = 2\n"))
        while x > 2 or x < 0:
            print("incorrect input")
            x = int(input(player.name + " Outside = 0, Center = 1, Inside = 2\n"))
        y = int(input("0 - 7 Clockwise\n"))
        while y > 7 or y < 0:
            print("incorrect input")
            y = int(input("0 - 7 Clockwise\n"))
        if legal_moves.__contains__(x.__str__() + y.__str__()):
            board[x][y] = player.token
            if token_check(x, y):
                remove_token(player)
            valid_input = True
        else:
            print("invalid position\nthe legal moves are: " + legal_moves)


def remove_token(player):
    print_board()
    print("Select token to remove")
    valid_input = False
    while not valid_input:
        x = int(input(player.name + " Outside = 0, Center = 1, Inside = 2\n"))
        while x > 2 or x < 0:
            print("incorrect input")
            x = int(input(player.name + " Outside = 0, Center = 1, Inside = 2\n"))
        y = int(input("0 - 7 Clockwise\n"))
        while y > 7 or y < 0:
            print("incorrect input")
            y = int(input("0 - 7 Clockwise\n"))
        if board[x][y] == player.token:
            print("Cant remove your own token")
        if board[x][y] == 0:
            print("position empty")
        if token_check(x, y) and free_token_exits():
            print("Please select a free token")
        elif board[x][y] != 0 and board[x][y] != player.token:
            board[x][y] = 0
            valid_input = True


def check_token_count():
    if player1.current_player_tokens() < 3:
        print(player2.name + " wins")
        return True
    if player2.current_player_tokens() < 3:
        print(player1.name + " wins")
        return True
    return False


def phase_one():
    stones_placed = 0
    while stones_placed <= 17:
        print(stones_placed)
        if stones_placed % 2 == 0:
            input_and_validation(player1)
        else:
            input_and_validation(player2)
        print_board()
        stones_placed += 1


def phase_two():
    print_board()
    x = 3
    y = 8
    turn = 0
    turns_without_mill = 0
    while turns_without_mill < 20:
        if turn % 2 == 0:
            player = player1
        else:
            player = player2
        turn += 1
        valid_input = False
        if not player.has_legal_moves():
            print(player.name + " has no legal moves and loses")
            return
        print("Select token to move")
        while not valid_input:
            x = int(input(player.name + " Outside = 0, Center = 1, Inside = 2\n"))
            while x > 2 or x < 0:
                print("incorrect input")
                x = int(input(player.name + " Outside = 0, Center = 1, Inside = 2\n"))
            y = int(input("0 - 7 Clockwise\n"))
            while y > 7 or y < 0:
                print("incorrect input")
                y = int(input("0 - 7 Clockwise\n"))
            if board[x][y] != player.token:
                print("you can only move your own token")
            elif board[x][y] == 0:
                print("position empty")
            else:
                valid_input = True
        board[x][y] = 0
        move_token(player, x, y)
        print_board()
        if check():
            turns_without_mill = 0
        else:
            turns_without_mill += 1
        if check_token_count():
            return
    print("Draw")


def nmm_game():
    phase_one()
    phase_two()
