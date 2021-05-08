import pytest
from fixtures import solution
from magicmaze import Solution
from itertools import product

def generate_maze(max_x, max_y, walls):
    maze = {xy: None for xy in product(range(max_x), range(max_y))}
    for xy in walls:
        del maze[xy]
    return maze
def test_best_action_bomb():
    """

    ....
    oxo.
    wowp
    """
    maze = generate_maze(4, 4, [(2, 1), (2, 3)])
    powerups = [(0, 3)]
    crates = [(1,1),(1,3),(2,2)]
    my_pos = (1, 2)
    distance = Solution.calculate_distance(maze, my_pos, crates)
    action, score = Solution.next_action(my_pos, distance, crates, powerups,[],{}, maze)
    print(score)
    assert action == "bomb"

def test_no_action():
    my_pos= (8, 0)
    distance= {(0, 0): [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], (0, 1): [(0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], (0, 2): [(0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], (0, 3): [(0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], (0, 4): [(0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], (0, 5): [(0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], (0, 6): [(0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], (0, 7): [(0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], (0, 8): [(0, 8), (0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], (1, 0): [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], (1, 2): None, (1, 4): None, (1, 6): None, (1, 8): [(1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0)], (2, 0): [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], (2, 1): None, (2, 2): None, (2, 3): None, (2, 4): None, (2, 5): None, (2, 6): None, (2, 7): None, (2, 8): [(2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0)], (3, 0): [(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], (3, 2): None, (3, 4): None, (3, 6): None, (3, 8): [(3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0)], (4, 0): [(4, 0), (5, 0), (6, 0), (7, 0), (8, 0)], (4, 1): None, (4, 2): None, (4, 3): None, (4, 4): None, (4, 5): None, (4, 6): None, (4, 7): None, (4, 8): [(4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0)], (5, 0): [(5, 0), (6, 0), (7, 0), (8, 0)], (5, 2): None, (5, 4): None, (5, 6): None, (5, 8): [(5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0)], (6, 0): [(6, 0), (7, 0), (8, 0)], (6, 1): None, (6, 2): None, (6, 3): None, (6, 4): None, (6, 5): None, (6, 6): None, (6, 7): None, (6, 8): [(6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0)], (7, 0): [(7, 0), (8, 0)], (7, 2): None, (7, 4): None, (7, 6): None, (7, 8): [(7, 8), (8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0)], (8, 0): [(8, 0)], (8, 1): [(8, 1), (8, 0)], (8, 2): [(8, 2), (8, 1), (8, 0)], (8, 3): [(8, 3), (8, 2), (8, 1), (8, 0)], (8, 4): [(8, 4), (8, 3), (8, 2), (8, 1), (8, 0)], (8, 5): [(8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0)], (8, 6): [(8, 6), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0)], (8, 7): [(8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0)], (8, 8): [(8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0)]}
    crates= [(2, 1), (4, 1), (6, 1), (1, 2), (3, 2), (5, 2), (7, 2), (2, 3), (4, 3), (6, 3), (1, 4), (3, 4), (5, 4), (7, 4), (2, 5), (4, 5), (6, 5), (1, 6), (3, 6), (5, 6), (7, 6), (2, 7), (4, 7), (6, 7)]
    powerups= [(2, 2), (4, 2), (6, 2), (2, 4), (4, 4), (6, 4), (2, 6), (4, 6), (6, 6)]
    vortexes= []
    players= {'Elf': '0,0', 'Knight': '8,0', 'Princess': '0,8', 'Meduza': '8,8'}
    maze= {(0, 0): None, (0, 1): None, (0, 2): None, (0, 3): None, (0, 4): None, (0, 5): None, (0, 6): None, (0, 7): None, (0, 8): None, (1, 0): None, (1, 2): None, (1, 4): None, (1, 6): None, (1, 8): None, (2, 0): None, (2, 1): None, (2, 2): None, (2, 3): None, (2, 4): None, (2, 5): None, (2, 6): None, (2, 7): None, (2, 8): None, (3, 0): None, (3, 2): None, (3, 4): None, (3, 6): None, (3, 8): None, (4, 0): None, (4, 1): None, (4, 2): None, (4, 3): None, (4, 4): None, (4, 5): None, (4, 6): None, (4, 7): None, (4, 8): None, (5, 0): None, (5, 2): None, (5, 4): None, (5, 6): None, (5, 8): None, (6, 0): None, (6, 1): None, (6, 2): None, (6, 3): None, (6, 4): None, (6, 5): None, (6, 6): None, (6, 7): None, (6, 8): None, (7, 0): None, (7, 2): None, (7, 4): None, (7, 6): None, (7, 8): None, (8, 0): None, (8, 1): None, (8, 2): None, (8, 3): None, (8, 4): None, (8, 5): None, (8, 6): None, (8, 7): None, (8, 8): None}
    action, score = Solution.next_action(my_pos, distance, crates, powerups, vortexes, players, maze)
    assert action != (0,0)

def test_no_action_1():
    pass
