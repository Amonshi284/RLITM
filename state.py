import numpy as np
import player
from ned import tictactoe_place

BOARD_ROWS_COLS = 3

class State:
    def __init__(self, p1, p2):
        self.board = np.zeros((BOARD_ROWS_COLS, BOARD_ROWS_COLS))
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHash = None
        self.playerSymbol = 1

    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_ROWS_COLS * BOARD_ROWS_COLS))
        return self.boardHash

    def availablePositions(self):
        positions = []
        for i in range(BOARD_ROWS_COLS):
            for j in range(BOARD_ROWS_COLS):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions

    def updateState(self, position):
        self.board[position] = self.playerSymbol
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    def winner(self):
        for i in range(BOARD_ROWS_COLS):
            if sum(self.board[i,:]) == 3:
                self.isEnd = True
                return 1
            if sum(self. board[i, :]) == -3:
                self.isEnd = True
                return -1

        for i in range(BOARD_ROWS_COLS):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1

        diag_sum1 = sum([self.board[i, i] for i in range(BOARD_ROWS_COLS)])
        diag_sum2 = sum([self.board[i, BOARD_ROWS_COLS - i - 1] for i in range(BOARD_ROWS_COLS)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1

        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0

        self.isEnd = False
        return None

    def giveReward(self):
        result = self.winner()

        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.2)

    def play(self, rounds=100):
        for i in range(rounds):
            if i % 1000 == 0:
                print("Rounds {}".format(i))
            while not self.isEnd:
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                self.updateState(p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)

                win = self.winner()
                if win is not None:
                    self.showBoard()
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
                else:
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)

                    win = self.winner()
                    if win is not None:
                        self.showBoard()
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    def play2(self):
        while not self.isEnd:
            # Player 1
            positions = self.availablePositions()
            p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
            # take action and update board state

            if isinstance(self.p1, player.Player):
                point = 0
                if p1_action == (0, 0):
                    point = 1
                elif p1_action == (0, 1):
                    point = 2
                elif p1_action == (0, 2):
                    point = 3
                elif p1_action == (1, 0):
                    point = 4
                elif p1_action == (1, 1):
                    point = 5
                elif p1_action == (1, 2):
                    point = 6
                elif p1_action == (2, 0):
                    point = 7
                elif p1_action == (2, 1):
                    point = 8
                elif p1_action == (2, 2):
                    point = 9
                tictactoe_place(point)
            self.updateState(p1_action)
            self.showBoard()
            # check board status if it is ended
            win = self.winner()
            if win is not None:
                self.giveReward()
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                # Player 2
                positions = self.availablePositions()
                p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                if isinstance(self.p2, player.Player):
                    point = 0
                    if p2_action == (0, 0):
                        point = 1
                    elif p2_action == (0, 1):
                        point = 2
                    elif p2_action == (0, 2):
                        point = 3
                    elif p2_action == (1, 0):
                        point = 4
                    elif p2_action == (1, 1):
                        point = 5
                    elif p2_action == (1, 2):
                        point = 6
                    elif p2_action == (2, 0):
                        point = 7
                    elif p2_action == (2, 1):
                        point = 8
                    elif p2_action == (2, 2):
                        point = 9
                    tictactoe_place(point)

                self.updateState(p2_action)
                self.showBoard()
                win = self.winner()
                if win is not None:
                    self.giveReward()
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break

    def reset(self):
        self.board = np.zeros((BOARD_ROWS_COLS, BOARD_ROWS_COLS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    def showBoard(self):
        for i in range(0, BOARD_ROWS_COLS):
            print('-------------')
            out = '| '
            for j in range(0, BOARD_ROWS_COLS):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')
