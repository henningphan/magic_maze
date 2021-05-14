import pytest
from pprint import pprint
from fixtures import solution
from magicmaze import Solution, State
import magicmaze as mm
from itertools import product

def test_neighbours():
    max_x = 6
    max_y = 6
    state = State()
    state.init_map(max_x, max_y, [])
    for xy in product([0, max_x-1], [0, max_y-1]):
        neigh = mm.neighbours(state, xy)
        assert len(neigh) == 2

def test_calculate_distance_no_blocks():
    """test calculate distance when the whole map is clear from obstacles"""
    max_x = 6
    max_y = 6
    state = State()
    state.avatar = "elf"
    state.init_players({"elf": "(0,0)"})
    state.init_map(max_x, max_y, [])
    for xy in product(range(max_x), range(max_y)):
        for xy2 in product(range(max_x), range(max_y)):
            state.update_players({"elf": str(xy)})
            distance = mm.calculate_distance(state, xy)
            assert len(distance[xy2]) == abs(xy2[0]-xy[0]) + abs(xy2[1]-xy[1]) + 1

def test_calculate_distance_w_blocks():
    """test calculate distance when the whole map with obstacles"""
    max_x = 6
    max_y = 1
    state = State()
    state.avatar = "elf"
    state.init_players({"elf": "(0,0)"})
    state.init_map(max_x, max_y, ["(1,0)"])
    distance = mm.calculate_distance(state, (0, 0))
    print(distance[(2,0)])
    assert distance[(2,0)] is None

def test_move_to():
    max_x = 6
    max_y = 6

    state = State()
    state.init_map(max_x, max_y, [])
    state.avatar = "elf"
    state.init_players({"elf": "(0,0"})
    distance = mm.calculate_distance(state, (0, 0))
    x, y = Solution.move_to(distance, (0,0))
    assert x == 0
    assert y == 0
    x, y = Solution.move_to(distance, (0,1))
    assert x == 0
    assert y == 1
    x, y = Solution.move_to(distance, (1,0))
    assert x == 1
    assert y == 0
    x, y = Solution.move_to(distance, (1,1))
    assert x+y == 1

def test_state_calculate_distance():
    state = State()
    state.init_map(6,6,[])
    state.avatar="elf"
    state.init_players({"elf": "(0,0)"})
    distance = mm.calculate_distance(state, (0,0))
    assert len(distance) == 36
    
def test_update_powerups():
    state = State()
    state.avatar="elf"
    state.init_players({"elf": "(0,0)"})
    assert state.my_power == 1
    state.update_powerups(["(0,0)"])
    assert state.my_power == 2
    state.update_powerups(["(0,0)"])
    assert state.my_power == 3

def test_update_vortexes_basic():
    """One player puts down one vortex"""
    state = State()
    state.avatar = "elf"
    state.init_players({"elf": "0,0"})
    state.update_vortexes(["0,0"])
    assert len(state.vortexes) == 1
    state.update_vortexes(["0,0"])
    assert len(state.vortexes) == 2

def test_update_vortexes_advanced():
    """
    One player puts down one vortex
    and there is a preexisting vortex
    """
    state = State()
    state.avatar = "elf"
    state.init_players({"elf": "0,0"})
    state.vortexes.append([State.Vort((0,1), 1, 1)])
    state.update_vortexes(["0,0", "0,1"])
    assert len(state.vortexes[-1]) == 2
    state.update_vortexes(["0,0", "0,1"])
    assert len(state.vortexes[-1]) == 2
    state.update_vortexes(["0,0"])
    assert len(state.vortexes[-1]) == 1

def test_heatmap():
    state = State()
    state.avatar = "elf"
    state.init_players({"elf": "0,0"})
    state.init_map(6,6, [])
    state.vortexes.append([State.Vort((0,1), 1, 1), State.Vort((0,0), 5, 5)])
    heatmap = create_heatmap(state)


def test_bomb_map():
    state = State()
    state.init_map(6,6, [])
    abc = mm.bomb_map(state, State.Vort((1,1),4,1))
    assert len(abc) == 11
    abc = mm.bomb_map(state, State.Vort((0,0),4,1))
    assert len(abc) == 9


def test_heatmap():
    state = State()
    state.init_map(6,6, [])
    state.vortexes.append([State.Vort((0,0),1,0), State.Vort((0,1),1, 2)])
    heatmap, future_vortexes = mm.create_heatmap(state)
    assert len(abc) == 11

