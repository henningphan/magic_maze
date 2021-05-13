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

def test_inaction():
    state = State()
    state.__dict__ = {'avatar': 'Elf', 'tick': 0, 'powerup': 1, 'crate': 5, 'player': 20, 'immolation': -10, 'maze': {(0, 0): None, (0, 2): None, (0, 3): None, (0, 4): None, (0, 6): None, (1, 0): None, (1, 1): None, (1, 2): None, (1, 3): None, (1, 4): None, (1, 5): None, (1, 6): None, (2, 0): None, (2, 1): None, (2, 2): None, (2, 3): None, (2, 4): None, (2, 5): None, (2, 6): None, (3, 1): None, (3, 2): None, (3, 3): None, (3, 4): None, (3, 5): None, (4, 0): None, (4, 1): None, (4, 2): None, (4, 3): None, (4, 4): None, (4, 5): None, (4, 6): None, (5, 0): None, (5, 1): None, (5, 2): None, (5, 3): None, (5, 4): None, (5, 5): None, (5, 6): None, (6, 0): None, (6, 2): None, (6, 3): None, (6, 4): None, (6, 6): None}, 'powerups': [[(0, 0), (1, 0), (2, 0), (4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6), (4, 6), (5, 6), (6, 6)], [(0, 0), (1, 0), (2, 0), (4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6), (4, 6), (5, 6), (6, 6)], [(0, 0), (1, 0), (2, 0), (4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6), (4, 6), (5, 6), (6, 6)], [(0, 0), (1, 0), (2, 0), (4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6), (4, 6), (5, 6), (6, 6)], [(0, 0), (1, 0), (4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6), (5, 6), (6, 6)], [(0, 0), (4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6), (6, 6)], [(4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6)], [(4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6)], [(4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6)], [(4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6)], [(4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6)], [(4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6)], [(4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6)], [(4, 0), (5, 0), (6, 0), (0, 6), (1, 6), (2, 6)]], 'vortexes': [[], [(2, 2), (4, 2), (2, 4), (4, 4)], [(2, 2), (4, 2), (2, 4), (4, 4)], [(2, 2), (4, 2), (2, 4), (4, 4)], [(2, 2), (4, 2), (1, 3), (2, 4), (4, 4)], [(2, 2), (4, 2), (1, 3), (2, 4), (4, 4)], [(2, 2), (4, 2), (1, 3), (2, 4), (4, 4)], [(1, 3)], [(2, 0), (1, 3)], [(2, 0), (1, 3)], [(2, 0)], [(2, 0), (3, 2)], [(2, 0), (3, 2)], [(2, 0), (3, 2)]], 'crates': [[(3, 2), (2, 3), (3, 3), (4, 3), (3, 4)], [(3, 2), (2, 3), (3, 3), (4, 3), (3, 4)], [(3, 2), (2, 3), (3, 3), (4, 3), (3, 4)], [(3, 2), (2, 3), (3, 3), (4, 3), (3, 4)], [(3, 2), (2, 3), (3, 3), (4, 3), (3, 4)], [(3, 2), (2, 3), (3, 3), (4, 3), (3, 4)], [(3, 2), (2, 3), (3, 3), (4, 3), (3, 4)], [(3, 3)], [(3, 3)], [(3, 3)], [(3, 3)], [(3, 3)], [(3, 3)], [(3, 3)]], 'power': [{'Meduza': 4, 'Knight': 1, 'Elf': 1, 'Princess': 4}], 'players': [{'Meduza': (2, 2), 'Knight': (4, 2), 'Elf': (2, 4), 'Princess': (4, 4)}, {'Meduza': (2, 2), 'Knight': (4, 2), 'Elf': (2, 4), 'Princess': (4, 4)}, {'Meduza': (2, 2), 'Knight': (4, 2), 'Elf': (2, 4), 'Princess': (4, 4)}, {'Meduza': (2, 1), 'Knight': (5, 2), 'Elf': (1, 4), 'Princess': (4, 5)}, {'Meduza': (2, 0), 'Knight': (6, 2), 'Elf': (1, 3), 'Princess': (4, 6)}, {'Meduza': (1, 0), 'Knight': (5, 2), 'Elf': (1, 3), 'Princess': (5, 6)}, {'Meduza': (0, 0), 'Knight': (4, 2), 'Elf': (0, 3), 'Princess': (6, 6)}, {'Meduza': (1, 0), 'Elf': (0, 2), 'Knight': (5, 2), 'Princess': (5, 6)}, {'Meduza': (2, 0), 'Elf': (0, 2), 'Knight': (6, 2), 'Princess': (5, 5)}, {'Meduza': (2, 0), 'Elf': (1, 2), 'Knight': (5, 2), 'Princess': (5, 6)}, {'Elf': (1, 1), 'Meduza': (2, 1), 'Knight': (4, 2), 'Princess': (6, 6)}, {'Elf': (1, 0), 'Meduza': (2, 0), 'Knight': (3, 2), 'Princess': (5, 6)}, {'Elf': (0, 0), 'Meduza': (2, 0), 'Knight': (3, 2), 'Princess': (5, 5)}, {'Elf': (0, 0), 'Meduza': (2, 0), 'Knight': (2, 2), 'Princess': (5, 6)}, {'Elf': (0, 0), 'Meduza': (2, 0), 'Knight': (1, 2), 'Princess': (6, 6)}]}
    action, score = next_action(state)
    assert score > 0
