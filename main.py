from pyniryo import *
from player import Player
from player import HumanPlayer
from state import State
from nine_mens_morris import nmm_game


# - Constants
BOARD_ROWS_COLS = 3

if __name__ == "__main__":

    game_selected = 0
    game_selected = int(input("Select game:\nTic Tac Toe = 1\nNine Mens Morris = 2"))

    if game_selected != 2:
        p1 = Player("p1")
        p1.loadPolicy("policy_p2")
        p2 = Player("p2")
        p2.loadPolicy("policy_p1")

        st = State(p1, p2)
        # st.play(5000)
        p2.savePolicy()
        p1.savePolicy()

        p2 = Player("p2", exp_rate=0)
        p2.loadPolicy("policy_p2")
        p1 = HumanPlayer("human")
        st = State(p1, p2)
        st.play2()
        p1.savePolicy()
        p2.savePolicy()
    else:
        nmm_game()
