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
    players = {"elf": "(1,2)"}
    crates = ["(1,1)","(1,3)", "(2,2)"]
    powerups = ["(0, 3)"]
    state.init_players(players)
    state.init_map(4,4, ["2,1", "2,3"])
    state.update_all(crates, powerups, [], players)
    action = mm.next_action(state)
    assert action.name == "bomb"


def test_penalty_table():
    state = State()
    state.avatar = "elf"
    players = {"elf": "(0,0)"}
    state.init_players(players)
    state.init_map(1,1, [])
    state.update_all([], [], [], players)
    action = mm.next_action(state)

    assert action.score >= 0

def test_flee_no():
    """

    ....
    oxo.
    wowp
    """
    state = State()
    state.avatar = "elf"
    state.init_players({"elf": "(2,0)"})
    state.init_map(6,1, [])
    state.update_crates([])
    state.vortexes = [[State.Vort((2,0), 1, 0)]]
    penalty = mm.is_dying(state, 5)
    assert penalty == 1

def test_flee_no_impossible():
    """

    ....
    oxo.
    wowp
    """
    state = State()
    state.avatar = "elf"
    state.init_players({"elf": "(2,0)"})
    state.init_map(6,1, [])
    state.update_crates([])
    state.vortexes = [[State.Vort((2,0), 8, 3)]]
    penalty = mm.is_dying(state, 5)
    assert penalty == 1

def test_flee_yes():
    state = State()
    state.avatar = "elf"
    state.init_players({"elf": "(2,0)"})
    state.init_map(6,1, [])
    state.update_crates([])
    state.vortexes = [[State.Vort((2,0), 1, 2)]]
    penalty = mm.is_dying(state, 5)
    assert penalty == 0

def test_flee_yes_unblocked():
    """avatar will die by a vortex, but
    a vortex will go off before destroying a crate
    thus allow avatar to escape
    0: bcpb
    1: xxpb
    2: opxx
    """
    state = State()
    state.avatar = "elf"
    state.init_players({"elf": "(2,0)"})
    state.init_map(3,1, [])
    state.update_crates(["1,0"])
    state.vortexes = [[State.Vort((0,0), 1,1), State.Vort((3,0), 2, 2)]]
    penalty = mm.is_dying(state, 5)
    assert penalty == 0

def test_flee_no_blocked():
    """avatar will die by a vortex, but
    a vortex will go off before destroying a crate
    thus allow avatar to escape
    """
    state = State()
    state.avatar = "elf"
    state.init_players({"elf": "(2,0)"})
    state.init_map(3,1, [])
    state.update_crates(["1,0"])
    state.vortexes = [[State.Vort((0,0), 1,1), State.Vort((2,0), 3, 2)]]
    penalty = mm.is_dying(state, 5)
    assert penalty == 1

def test_adhoc():
    state = State()
    state.__dict__ = {'avatar': 'Meduza', 'tick': 0, 'powerup': 1, 'crate': 5, 'player': 20, 'immolation': -10, 'maze': {(0, 0): None, (0, 1): None, (0, 2): None, (0, 3): None, (0, 4): None, (0, 6): None, (0, 7): None, (0, 8): None, (0, 9): None, (0, 10): None, (1, 0): None, (1, 4): None, (1, 6): None, (1, 10): None, (2, 0): None, (2, 2): None, (2, 3): None, (2, 4): None, (2, 6): None, (2, 7): None, (2, 8): None, (2, 10): None, (3, 0): None, (3, 2): None, (3, 4): None, (3, 6): None, (3, 8): None, (3, 10): None, (4, 0): None, (4, 1): None, (4, 2): None, (4, 4): None, (4, 5): None, (4, 6): None, (4, 8): None, (4, 9): None, (4, 10): None, (5, 4): None, (5, 5): None, (5, 6): None, (6, 0): None, (6, 1): None, (6, 2): None, (6, 4): None, (6, 5): None, (6, 6): None, (6, 8): None, (6, 9): None, (6, 10): None, (7, 0): None, (7, 2): None, (7, 4): None, (7, 6): None, (7, 8): None, (7, 10): None, (8, 0): None, (8, 2): None, (8, 3): None, (8, 4): None, (8, 6): None, (8, 7): None, (8, 8): None, (8, 10): None, (9, 0): None, (9, 4): None, (9, 6): None, (9, 10): None, (10, 0): None, (10, 1): None, (10, 2): None, (10, 3): None, (10, 4): None, (10, 6): None, (10, 7): None, (10, 8): None, (10, 9): None, (10, 10): None}, 'powerups': [[(4, 4), (5, 4), (6, 4), (4, 5), (5, 5), (6, 5), (4, 6), (5, 6), (6, 6)], [(4, 4), (5, 4), (6, 4), (4, 5), (5, 5), (6, 5), (4, 6), (5, 6), (6, 6)], [(4, 4), (5, 4), (6, 4), (4, 5), (5, 5), (6, 5), (4, 6), (5, 6), (6, 6)], [(4, 4), (5, 4), (6, 4), (4, 5), (5, 5), (6, 5), (4, 6), (5, 6), (6, 6)], [(4, 4), (5, 4), (6, 4), (4, 5), (5, 5), (6, 5), (4, 6), (5, 6), (6, 6)], [(4, 4), (5, 4), (6, 4), (4, 5), (5, 5), (6, 5), (4, 6), (5, 6), (6, 6)], [(4, 4), (5, 4), (6, 4), (4, 5), (5, 5), (6, 5), (4, 6), (5, 6), (6, 6)], [(4, 4), (5, 4), (6, 4), (4, 5), (5, 5), (6, 5), (4, 6), (5, 6), (6, 6)], [(4, 4), (5, 4), (6, 4), (4, 5), (5, 5), (6, 5), (4, 6), (5, 6), (6, 6)], [(5, 4), (6, 4), (4, 5), (5, 5), (6, 5), (5, 6)], [(5, 4), (6, 4), (5, 5), (6, 5)], [(5, 4), (6, 4), (6, 5)], [(6, 4), (6, 5)], [(6, 4), (6, 5)], [(6, 5)], [(6, 5)], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], 'players': [{'Knight': (0, 0), 'Elf': (10, 0), 'Princess': (0, 10), 'Meduza': (10, 10)}, {'Knight': (0, 0), 'Elf': (10, 0), 'Princess': (0, 10), 'Meduza': (10, 10)}, {'Elf': (9, 0), 'Knight': (0, 1), 'Princess': (0, 9), 'Meduza': (10, 9)}, {'Elf': (8, 0), 'Knight': (0, 2), 'Princess': (0, 8), 'Meduza': (10, 8)}, {'Elf': (7, 0), 'Knight': (0, 3), 'Princess': (0, 7), 'Meduza': (10, 7)}, {'Elf': (6, 0), 'Knight': (0, 4), 'Princess': (0, 6), 'Meduza': (10, 6)}, {'Elf': (6, 1), 'Knight': (1, 4), 'Princess': (1, 6), 'Meduza': (9, 6)}, {'Elf': (6, 2), 'Knight': (2, 4), 'Princess': (2, 6), 'Meduza': (8, 6)}, {'Elf': (7, 2), 'Knight': (3, 4), 'Princess': (3, 6), 'Meduza': (7, 6)}, {'Elf': (8, 2), 'Knight': (4, 4), 'Princess': (4, 6), 'Meduza': (6, 6)}, {'Elf': (8, 3), 'Knight': (4, 4), 'Princess': (4, 5), 'Meduza': (5, 6)}, {'Knight': (4, 4), 'Elf': (8, 4), 'Princess': (4, 5), 'Meduza': (5, 5)}, {'Knight': (4, 4), 'Meduza': (5, 4), 'Elf': (9, 4), 'Princess': (5, 5)}, {'Meduza': (5, 4), 'Elf': (10, 4), 'Knight': (4, 5), 'Princess': (5, 5)}, {'Elf': (10, 3), 'Meduza': (6, 4), 'Knight': (4, 6), 'Princess': (5, 6)}, {'Elf': (10, 2), 'Meduza': (6, 4), 'Knight': (3, 6), 'Princess': (5, 6)}, {'Elf': (10, 1), 'Meduza': (6, 5), 'Knight': (2, 6), 'Princess': (5, 6)}, {'Elf': (10, 0), 'Meduza': (6, 5), 'Princess': (5, 6), 'Knight': (2, 7)}, {'Elf': (10, 1), 'Meduza': (5, 5), 'Princess': (5, 6), 'Knight': (2, 8)}, {'Elf': (10, 2), 'Meduza': (4, 5), 'Princess': (5, 6), 'Knight': (3, 8)}, {'Elf': (10, 3), 'Meduza': (4, 4), 'Princess': (5, 6), 'Knight': (2, 8)}, {'Meduza': (3, 4), 'Elf': (10, 4), 'Knight': (2, 7)}, {'Elf': (10, 3), 'Meduza': (2, 4), 'Knight': (2, 8)}, {'Elf': (10, 2), 'Meduza': (1, 4), 'Knight': (3, 8)}, {'Elf': (10, 1), 'Meduza': (0, 4), 'Knight': (2, 8)}, {'Elf': (10, 0), 'Meduza': (0, 3), 'Knight': (2, 7)}, {'Elf': (10, 1), 'Meduza': (0, 2), 'Knight': (2, 8)}, {'Meduza': (0, 1), 'Elf': (10, 2), 'Knight': (3, 8)}, {'Meduza': (0, 0), 'Elf': (10, 3), 'Knight': (2, 8)}, {'Meduza': (0, 0), 'Elf': (10, 4), 'Knight': (2, 7)}, {'Meduza': (0, 0), 'Elf': (9, 4), 'Knight': (2, 8)}, {'Meduza': (0, 0), 'Elf': (8, 4), 'Knight': (3, 8)}, {'Meduza': (0, 0), 'Elf': (7, 4), 'Knight': (2, 8)}, {'Meduza': (0, 0), 'Elf': (6, 4), 'Knight': (2, 7)}, {'Meduza': (0, 0), 'Elf': (5, 4), 'Knight': (2, 8)}, {'Meduza': (0, 0), 'Elf': (4, 4), 'Knight': (3, 8)}, {'Meduza': (0, 0), 'Elf': (3, 4), 'Knight': (2, 8)}, {'Meduza': (0, 0), 'Elf': (2, 4), 'Knight': (2, 7)}, {'Meduza': (0, 0), 'Elf': (1, 4), 'Knight': (2, 8)}, {'Meduza': (0, 0), 'Elf': (0, 4), 'Knight': (3, 8)}, {'Meduza': (0, 0), 'Elf': (0, 3), 'Knight': (2, 8)}, {'Meduza': (0, 0), 'Elf': (0, 2), 'Knight': (2, 7)}, {'Meduza': (0, 0), 'Elf': (0, 1), 'Knight': (2, 8)}, {'Meduza': (0, 0), 'Elf': (0, 1), 'Knight': (3, 8)}, {'Meduza': (0, 0), 'Elf': (0, 2), 'Knight': (2, 8)}, {'Meduza': (0, 0), 'Elf': (0, 3), 'Knight': (2, 7)}, {'Meduza': (0, 0), 'Elf': (0, 4), 'Knight': (2, 8)}, {'Meduza': (0, 0), 'Elf': (1, 4), 'Knight': (3, 8)}], 'vortexes': [[], [], [], [], [], [], [], [], [], [], [Vort(pos=(4, 4), power=2, time=5)], [Vort(pos=(4, 4), power=2, time=4)], [Vort(pos=(4, 4), power=2, time=3)], [Vort(pos=(4, 4), power=2, time=2)], [Vort(pos=(4, 4), power=2, time=1), Vort(pos=(5, 6), power=3, time=5)], [Vort(pos=(4, 4), power=2, time=0), Vort(pos=(5, 6), power=3, time=4)], [Vort(pos=(5, 6), power=3, time=3)], [Vort(pos=(5, 6), power=3, time=2)], [Vort(pos=(5, 6), power=3, time=1)], [Vort(pos=(5, 6), power=3, time=0)], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [Vort(pos=(0, 1), power=1, time=5)], [Vort(pos=(0, 1), power=1, time=4)], [Vort(pos=(0, 1), power=1, time=3)], [Vort(pos=(0, 1), power=1, time=2)], [Vort(pos=(0, 1), power=1, time=1)]], 'heatmap': {(0, 0): None, (0, 1): None, (0, 2): None, (0, 3): None, (0, 4): None, (0, 6): None, (0, 7): None, (0, 8): None, (0, 9): None, (0, 10): None, (1, 0): None, (1, 4): None, (1, 6): None, (1, 10): None, (2, 0): None, (2, 2): None, (2, 3): None, (2, 4): None, (2, 6): None, (2, 7): None, (2, 8): None, (2, 10): None, (3, 0): None, (3, 2): None, (3, 4): None, (3, 6): None, (3, 8): None, (3, 10): None, (4, 0): None, (4, 1): None, (4, 2): None, (4, 4): None, (4, 5): None, (4, 6): None, (4, 8): None, (4, 9): None, (4, 10): None, (5, 4): None, (5, 5): None, (5, 6): None, (6, 0): None, (6, 1): None, (6, 2): None, (6, 4): None, (6, 5): None, (6, 6): None, (6, 8): None, (6, 9): None, (6, 10): None, (7, 0): None, (7, 2): None, (7, 4): None, (7, 6): None, (7, 8): None, (7, 10): None, (8, 0): None, (8, 2): None, (8, 3): None, (8, 4): None, (8, 6): None, (8, 7): None, (8, 8): None, (8, 10): None, (9, 0): None, (9, 4): None, (9, 6): None, (9, 10): None, (10, 0): None, (10, 1): None, (10, 2): None, (10, 3): None, (10, 4): None, (10, 6): None, (10, 7): None, (10, 8): None, (10, 9): None, (10, 10): None}, 'crates': [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], 'power': [{'Knight': 2, 'Elf': 1, 'Princess': 3, 'Meduza': 7}]}
    actions = mm.next_action(state)
    import pdb
    pdb.set_trace()
    assert actions[0].name == (0,0)

