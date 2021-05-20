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
    state.update_players(players)
    state.init_map(4,4, ["2,1", "2,3"])
    state.update_all(crates, powerups, [], players)
    actions = mm.next_action(state)
    assert actions[0].name == "bomb"


def test_cant_escape_bomb():
    """
   (p,b)
    x
    x
    x
    x
    """
    state = State()
    state.avatar = "elf"
    players = {"elf": "0,0"}
    state.update_players(players)
    state.init_map(5,1, [])
    state.vortexes = [Vort((0,0),1,1)]
    actions = mm.next_action(state)
    assert actions[0].score < 0

def test_penalty_table():
    state = State()
    state.avatar = "elf"
    players = {"elf": "(0,0)"}
    state.update_players(players)
    state.init_map(1,1, [])
    state.update_all([], [], [], players)
    actions = mm.next_action(state)

    assert actions[0].score >= 0

def test_flee_no():
    """
    x
    x
    (p,b)
    x
    x
    x
    """
    state = State()
    state.avatar = "elf"
    state.update_players({"elf": "(2,0)"})
    state.init_map(6,1, [])
    state.update_crates([])
    state.vortexes = [Vort((2,0), 1, 0)]
    bomb_crates = calc_bomb_crates(state)
    penalty = mm.is_dying(state, bomb_crates, 5)
    assert penalty == 1

def test_flee_no_impossible():
    """
    x
    (p,b)
    x
    x
    x
    x
    """
    state = State()
    state.avatar = "elf"
    state.update_players({"elf": "(2,0)"})
    state.init_map(6,1, [])
    state.update_crates([])
    state.vortexes = [Vort((2,0), 8, 3)]
    bomb_crates = calc_bomb_crates(state)
    penalty = mm.is_dying(state, bomb_crates, 5)
    assert penalty == 1

def test_flee_yes():
    state = State()
    state.avatar = "elf"
    state.update_players({"elf": "(2,0)"})
    state.init_map(6,1, [])
    state.update_crates([])
    state.vortexes = [Vort((2,0), 1, 2)]
    penalty = mm.is_dying(state, 5)
    assert penalty == 0

def test_flee_yes_unblocked():
    """avatar is threatened by a vortex1, but
    a vortex2 will go off before destroying a crate
    thus allow avatar to escape

    b
    c
    (p,b)
    x
    """
    state = State()
    state.avatar = "elf"
    state.update_players({"elf": "(2,0)"})
    state.init_map(3,1, [])
    state.update_crates(["1,0"])
    state.vortexes = [Vort((0,0), 1,1), Vort((2,0), 1, 3)]
    bomb_crates = calc_bomb_crates(state)
    import pdb
    pdb.set_trace()
    penalty = mm.is_dying(state, bomb_crates, 5)
    assert penalty == 0

def test_flee_no_blocked():
    """avatar will die by a vortex, but
    a vortex will go off before destroying a crate
    thus allow avatar to escape
    """
    state = State()
    state.avatar = "elf"
    state.update_players({"elf": "(2,0)"})
    state.init_map(3,1, [])
    state.update_crates(["1,0"])
    state.vortexes = [Vort((0,0), 1,1), Vort((2,0), 3, 2)]
    bomb_crates = calc_bomb_crates(state)
    penalty = mm.is_dying(state, bomb_crates, 5)
    assert penalty == 1

def test_adhoc():
    state = State()
    state.__dict__ = {'avatar': 'Princess', 'tick': 0, 'powerup': 1, 'crate': 5, 'player': 20, 'immolation': -10, 'maze': {(0, 0): None, (0, 1): None, (0, 2): None, (0, 3): None, (0, 4): None, (0, 5): None, (0, 6): None, (0, 7): None, (0, 8): None, (1, 0): None, (1, 2): None, (1, 4): None, (1, 6): None, (1, 8): None, (2, 0): None, (2, 1): None, (2, 2): None, (2, 3): None, (2, 4): None, (2, 5): None, (2, 6): None, (2, 7): None, (2, 8): None, (3, 0): None, (3, 2): None, (3, 4): None, (3, 6): None, (3, 8): None, (4, 0): None, (4, 1): None, (4, 2): None, (4, 3): None, (4, 4): None, (4, 5): None, (4, 6): None, (4, 7): None, (4, 8): None, (5, 0): None, (5, 2): None, (5, 4): None, (5, 6): None, (5, 8): None, (6, 0): None, (6, 1): None, (6, 2): None, (6, 3): None, (6, 4): None, (6, 5): None, (6, 6): None, (6, 7): None, (6, 8): None, (7, 0): None, (7, 2): None, (7, 4): None, (7, 6): None, (7, 8): None, (8, 0): None, (8, 1): None, (8, 2): None, (8, 3): None, (8, 4): None, (8, 5): None, (8, 6): None, (8, 7): None, (8, 8): None}, 'powerups': [(2, 2), (4, 2), (6, 2), (4, 4), (6, 4), (2, 5), (3, 6), (4, 6), (6, 6), (6, 7)], 'players': {'Princess': (2, 2)}, 'vortexes': [Vort(pos=(0, 4), power=3, time=1), Vort(pos=(2, 4), power=4, time=4)], 'crates': [(2, 1), (4, 1), (6, 1), (3, 2), (5, 2), (4, 3), (6, 3), (3, 4), (5, 4), (4, 5), (6, 5)], 'power': {'Princess': 5, 'Meduza': 1, 'Knight': 1, 'Elf': 1}, 'phantoms': [{(0, 8), (8, 0), (0, 0)}, {(0, 1), (0, 7), (8, 1)}, {(8, 2), (0, 2), (0, 6)}, {(8, 2), (0, 2), (0, 6)}, {(8, 3), (0, 3), (0, 5)}, {(8, 4), (0, 3), (0, 4)}, {(8, 4), (0, 3), (0, 4)}, {(0, 2), (8, 5), (0, 5)}, {(0, 1), (8, 6), (0, 6)}, {(8, 6), (0, 0)}, {(0, 1), (8, 5)}, {(0, 2), (8, 6)}, {(0, 3), (8, 6)}, {(0, 4), (8, 6)}, {(0, 5), (8, 6)}, {(0, 6)}, {(0, 6)}, {(0, 7)}, {(0, 8)}, {(0, 7)}, {(0, 7)}, set(), set(), set(), set(), set(), set(), set()], 'phantom_cache': set()}
    actions = next_action(state)
    assert actions[0].name == (-1, 0)
