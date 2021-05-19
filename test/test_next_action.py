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
    import pdb
    pdb.set_trace()
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

    ....
    oxo.
    wowp
    """
    state = State()
    state.avatar = "elf"
    state.update_players({"elf": "(2,0)"})
    state.init_map(6,1, [])
    state.update_crates([])
    state.vortexes = [Vort((2,0), 1, 0)]
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
    state.update_players({"elf": "(2,0)"})
    state.init_map(6,1, [])
    state.update_crates([])
    state.vortexes = [Vort((2,0), 8, 3)]
    penalty = mm.is_dying(state, 5)
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
    """avatar will die by a vortex, but
    a vortex will go off before destroying a crate
    thus allow avatar to escape
    0: bcpb
    1: xxpb
    2: opxx
    """
    state = State()
    state.avatar = "elf"
    state.update_players({"elf": "(2,0)"})
    state.init_map(3,1, [])
    state.update_crates(["1,0"])
    state.vortexes = [Vort((0,0), 1,1), Vort((2,0), 1, 3)]
    penalty = mm.is_dying(state, 5)
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
    penalty = mm.is_dying(state, 5)
    assert penalty == 1

def test_adhoc():
    state = State()
    state.__dict__ = {'avatar': 'Elf', 'tick': 0, 'powerup': 1, 'crate': 5, 'player': 20, 'immolation': -10, 'maze': {(0, 0): None, (0, 2): None, (0, 3): None, (0, 4): None, (0, 6): None, (1, 0): None, (1, 1): None, (1, 2): None, (1, 3): None, (1, 4): None, (1, 5): None, (1, 6): None, (2, 0): None, (2, 1): None, (2, 2): None, (2, 3): None, (2, 4): None, (2, 5): None, (2, 6): None, (3, 1): None, (3, 2): None, (3, 3): None, (3, 4): None, (3, 5): None, (4, 0): None, (4, 1): None, (4, 2): None, (4, 3): None, (4, 4): None, (4, 5): None, (4, 6): None, (5, 0): None, (5, 1): None, (5, 2): None, (5, 3): None, (5, 4): None, (5, 5): None, (5, 6): None, (6, 0): None, (6, 2): None, (6, 3): None, (6, 4): None, (6, 6): None}, 'powerups': [(0, 0), (1, 0), (2, 0), (4, 6), (5, 6), (6, 6)], 'players': {'Knight': (5, 0), 'Elf': (1, 3), 'Meduza': (6, 3), 'Princess': (0, 6)}, 'vortexes': [Vort(pos=(2, 2), power=1, time=0), Vort(pos=(4, 2), power=1, time=0), Vort(pos=(2, 4), power=1, time=0), Vort(pos=(4, 4), power=1, time=0), Vort(pos=(1, 3), power=1, time=3)], 'heatmap': {(0, 0): None, (0, 2): None, (0, 3): None, (0, 4): None, (0, 6): None, (1, 0): None, (1, 1): None, (1, 2): None, (1, 3): None, (1, 4): None, (1, 5): None, (1, 6): None, (2, 0): None, (2, 1): None, (2, 2): None, (2, 3): None, (2, 4): None, (2, 5): None, (2, 6): None, (3, 1): None, (3, 2): None, (3, 3): None, (3, 4): None, (3, 5): None, (4, 0): None, (4, 1): None, (4, 2): None, (4, 3): None, (4, 4): None, (4, 5): None, (4, 6): None, (5, 0): None, (5, 1): None, (5, 2): None, (5, 3): None, (5, 4): None, (5, 5): None, (5, 6): None, (6, 0): None, (6, 2): None, (6, 3): None, (6, 4): None, (6, 6): None}, 'crates': [(3, 2), (2, 3), (3, 3), (4, 3), (3, 4)], 'power': {'Elf': 1, 'Knight': 4, 'Princess': 4, 'Meduza': 1}}
    actions = next_action(state)
    assert actions[0].score == 0
