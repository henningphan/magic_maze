import pytest
from fixtures import solution
from magicmaze import *
from itertools import product
import magicmaze as mm

def test_best_action_bomb():
    """

    ....
    oxo.
    wowp
    """
    state = State()
    state.avatar = "elf"
    state.init_players({"elf": "(1,2)"})
    state.init_map(4,4, ["2,1", "2,3"])
    state.update_powerups(["(0, 3)"])
    state.update_crates(["(1,1)","(1,3)", "(2,2)"])
    state.update_vortexes([])
    distance = mm.calculate_distance(state, state.my_pos)
    action, score = mm.next_action(state)
    print(score)
    assert action == "bomb"
