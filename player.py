import numpy as np
import pickle
import ned

BOARD_ROWS_COLS = 3


class Player:
    def __init__(self, name, exp_rate=0.3, learn_rate=0.2, decay_gamma=0.95):
        self.name = name
        self.states = []
        self.lr = learn_rate
        self.exp_rate = exp_rate
        self.decay_gamma = decay_gamma
        self.states_value = {}

    @staticmethod
    def get_hash(board):
        board_hash = str(board.reshape(BOARD_ROWS_COLS * BOARD_ROWS_COLS))
        return board_hash

    def choose_action(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) < self.exp_rate:
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.get_hash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)

                if value >= value_max:
                    value_max = value
                    action = p

        return action

    def add_state(self, state):
        self.states.append(state)

    def feed_reward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (reward - self.states_value[st])
            reward = self.states_value[st]
        self.lr = max(self.lr * self.decay_gamma, 0.01)

    def reset(self):
        self.states = []

    def save_policy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def load_policy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def choose_action(self, positions, _, __):
        return ned.find_new_pos(positions)

    # append a hash state
    def add_state(self, state):
        pass

    # at the end of game, backpropagate and update states value
    def feed_reward(self, reward):
        pass

    def save_policy(self):
        pass

    def reset(self):
        pass
