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

