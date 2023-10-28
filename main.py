from pyniryo import *
from player import Player
from player import HumanPlayer
from state import State
from nine_mens_morris import nmm_game

if __name__ == "__main__":

    game_selected = 0
    game_selected = int(input("Select game:\nTic Tac Toe = 1\nNine Mens Morris = 2"))

    if game_selected != 2:
        p1 = Player("p1")
        p1.load_policy("policy_p2")
        p2 = Player("p2")
        p2.load_policy("policy_p1")

        st = State(p1, p2)
        st.play(50)
        p2.save_policy()
        p1.save_policy()

        p1 = Player("p2", exp_rate=0)
        p1.load_policy("policy_p2")
        p2 = HumanPlayer("human")
        st = State(p1, p2)
        st.play2()
        p1.save_policy()
        p2.save_policy()
    else:
        nmm_game()
