from player import Player
from player import HumanPlayer
from state import State


# - Constants
BOARD_ROWS_COLS = 3

if __name__ == "__main__":

    p1 = Player("p1")
    p1.loadPolicy("policy_p2")
    p2 = Player("p2")
    p2.loadPolicy("policy_p1")

    st = State(p1, p2)
    # st.play(500)
    p2.savePolicy()
    p1.savePolicy()

    p2 = Player("p2", exp_rate=0)
    p2.loadPolicy("policy_p2")
    p1 = HumanPlayer("human")
    st = State(p1, p2)
    st.play2()

    p1.savePolicy()
    p2.savePolicy()
