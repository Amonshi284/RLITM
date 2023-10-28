from player import Player
from state import State

games = 10000
p1 = Player("p1", exp_rate=0)
p1.load_policy("policy_p2")
p2 = Player("p2", exp_rate=0)
p2.load_policy("policy_p1")
st = State(p1, p2)
st.play(games)
print(st.wins)
print(st.losses)
print((st.losses / games) * 100)
