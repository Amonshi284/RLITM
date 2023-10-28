import numpy as np

import ned
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
        self.losses = 0
        self.wins = 0

    def get_hash(self):
        self.boardHash = str(self.board.reshape(BOARD_ROWS_COLS * BOARD_ROWS_COLS))
        return self.boardHash

    # list open spaces
    def available_positions(self):
        positions = []
        for i in range(BOARD_ROWS_COLS):
            for j in range(BOARD_ROWS_COLS):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions

    def update_state(self, position):
        self.board[position] = self.playerSymbol
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    # check if one of the players has won
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

        if len(self.available_positions()) == 0:
            self.isEnd = True
            return 0

        self.isEnd = False
        return None

    def give_reward(self):
        result = self.winner()

        if result == 1:
            self.wins += 1
            self.p1.feed_reward(1)
            self.p2.feed_reward(0)
        elif result == -1:
            self.losses += 1
            self.p1.feed_reward(0)
            self.p2.feed_reward(1)
        else:
            self.p1.feed_reward(0.1)
            self.p2.feed_reward(0.2)

    def play(self, rounds=100):
        for i in range(rounds):
            if i % 1000 == 0:
                print("Rounds {}".format(i))
            while not self.isEnd:
                # give player 1 a list of open spaces and let him choose his action
                positions = self.available_positions()
                p1_action = self.p1.choose_action(positions, self.board, self.playerSymbol)
                self.update_state(p1_action)
                board_hash = self.get_hash()
                self.p1.add_state(board_hash)

                win = self.winner()
                if win is not None:
                    # show end state, give out rewards and reset for a new game
                    self.show_board()
                    self.give_reward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
                else:
                    # give player 2 a list of open spaces and let him choose his action
                    positions = self.available_positions()
                    p2_action = self.p2.choose_action(positions, self.board, self.playerSymbol)
                    self.update_state(p2_action)
                    board_hash = self.get_hash()
                    self.p2.add_state(board_hash)

                    win = self.winner()
                    if win is not None:
                        # show end state, give out rewards and reset for a new game
                        self.show_board()
                        self.give_reward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    def play2(self):
        while not self.isEnd:
            # Player 1
            self.playerturn(self.p1)
            # check board status if it is ended
            win = self.winner()
            if win is not None:
                self.give_reward()
                if win == 1:
                    print(self.p1.name, "wins!")
                    ned.robot.play_sound("mixkit-achievement-bell-600.wav")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                # Player 2
                self.playerturn(self.p2)
                # check board status if it is ended
                win = self.winner()
                if win is not None:
                    self.give_reward()
                    if win == -1:
                        print(self.p2.name, "wins!")
                        ned.robot.play_sound("mixkit-achievement-bell-600.wav")
                    else:
                        print("tie!")
                    self.reset()
                    break

    def playerturn(self, p):
        # Player 1
        positions = self.available_positions()
        p_action = p.choose_action(positions, self.board, self.playerSymbol)
        # take action and update board state

        if isinstance(p, player.Player):
            point = 0
            if p_action == (0, 0):
                point = 1
            elif p_action == (0, 1):
                point = 2
            elif p_action == (0, 2):
                point = 3
            elif p_action == (1, 0):
                point = 4
            elif p_action == (1, 1):
                point = 5
            elif p_action == (1, 2):
                point = 6
            elif p_action == (2, 0):
                point = 7
            elif p_action == (2, 1):
                point = 8
            elif p_action == (2, 2):
                point = 9
            tictactoe_place(point)
        self.update_state(p_action)
        self.show_board()

    def reset(self):
        self.board = np.zeros((BOARD_ROWS_COLS, BOARD_ROWS_COLS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    def show_board(self):
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
