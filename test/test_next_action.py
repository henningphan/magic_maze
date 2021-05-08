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
