import pytest
from fixtures import solution
from magicmaze import Solution
from itertools import product

def test_neighbours():
    max_x = 6
    max_y = 6
    maze = {xy: None for xy in product(range(max_x), range(max_y))}
    for xy in product([0, max_x-1], [0, max_y-1]):
        neigh = Solution.neighbours(xy, maze)
        assert len(neigh) == 2

def test_calculate_distance_no_blocks():
    """test calculate distance when the whole map is clear from obstacles"""
    max_x = 6
    max_y = 6
    maze = {xy: None for xy in product(range(max_x), range(max_y))}
    for xy in product(range(max_x), range(max_y)):
        for xy2 in product(range(max_x), range(max_y)):
            distance = Solution.calculate_distance(maze, xy, [])
            assert len(distance[xy2]) == abs(xy2[0]-xy[0]) + abs(xy2[1]-xy[1]) + 1

def test_move_to():
    max_x = 6
    max_y = 6
    maze = {xy: None for xy in product(range(max_x), range(max_y))}
    distance = Solution.calculate_distance(maze, (0, 0), [])
    x, y = Solution.move_to(distance, (0,0))
    assert y == 1


