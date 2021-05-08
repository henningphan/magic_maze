from itertools import product
from collections import namedtuple
from pprint import pprint

class Solution:
    def __init__(self, api):
        self.api = api
        self.powerup = -1
        self.crate = 5
        self.player = 20
        self.immolation = -10
        self.tick = 0


    def initialize_maze_data(self, maze_width, maze_height, walls,
your_avatar):
        """
        Before the first update is called this method will receive
static maze
        data, such as maze dimensions and which competitor you are

        :type maze_width: int
        :type maze_height: int
        :type walls: List[string]
        :type your_avatar: string
        """
        print("whoami: ", your_avatar)
        self.avatar = your_avatar
        self.maze = {xy: None for xy in product(range(maze_width),
range(maze_height))}

        for xy in (self.position(xy) for xy in walls):
            del self.maze[xy]

        assert maze_width == maze_height

    def position(self, str_pos):
        x, y = str_pos.replace("(","").replace(")","").split(",")
        return int(x), int(y)

    def update(self, crates, powerups, vortexes, players):
        """
        Executes a single step of Magic Maze logic. As a competitor it
is up
        to you to either move or place a magical explosion, you can't
do both
        in the same update. This function will be called repeatedly either
        until there is a winner or the time runs out!

        :type crates: List[string]
        :type powerups: List[string]
        :type vortexes: List[string]
        :type players: Dict[string, string]
        """
        self.tick += 1
        my_pos = self.position(players[self.avatar])
        print("whoami: ", self.avatar)
        pprint(my_pos)
        crates = [self.position(c) for c in crates]
        powerups = [self.position(p) for p in powerups if self.position(p) != my_pos]

        vortexes = [self.position(v) for v in vortexes]
        my_pos = self.position(players[self.avatar])

        distance = Solution.calculate_distance(self.maze, my_pos, crates)
        action, score = Solution.next_action(my_pos, distance, crates, powerups, vortexes, players, self.maze)
        print("best action: ", action)
        if action == "bomb":
            self.api.magical_explosion()
        else:
            pos = action
            self.api.move(*Solution.move_to(distance, pos))


    @staticmethod
    def calculate_distance(maze, my_pos, blocked_pos=None):
        """
        :type blocked_pos: Tuple(int, int), positions one cannot move to
        """
        blocked_pos = blocked_pos if blocked_pos else []
        distance = maze.copy()
        queue = [(my_pos, [])]
        while queue:
            pos, way = queue.pop(0)
            if distance[pos] is None:
                distance[pos] = [pos] + way
                new_way = [pos] + way
                neighbours = ((pos, new_way.copy()) for pos in
                        Solution.neighbours(pos, maze) if distance[pos] is None and pos not in blocked_pos)
                queue.extend(neighbours)
        return distance

    @staticmethod
    def neighbours(pos, maze):
        """
        :type pos: tuple(int, int)
        :type maze: dict[tuple(int int)] = None
        """
        all_neighbours = [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]),
                (pos[0], pos[1]-1), (pos[0], pos[1]+1)]
        valid_neighbours = [n for n in all_neighbours if n in maze]
        return valid_neighbours

    @staticmethod
    def move_to(distance, pos):
        """
        :type distance: maze with walking distance
        :type pos): tuple(int, int)
        """
        if len(distance[pos]) == 1:
            return (0,0)
        x1, y1 = distance[pos][-1]
        x2, y2 = distance[pos][-2]
        x_change = x2-x1
        y_change = y2-y1
        return (x_change, y_change)

    @staticmethod
    def next_action(my_pos, distance, crates, powerups, vortexes, players, maze):
        bomb_score = Solution.eval_bomb(my_pos, crates, vortexes)
        pos_score = [(pos, Solution.position_score(pos, distance, crates, powerups, vortexes, maze)) for pos in maze.copy().keys()]
        scores = pos_score + [bomb_score]
        scores.sort(key=lambda tup: tup[1], reverse=True)
        return scores[0]

        

    @staticmethod
    def eval_bomb(my_pos, crates, vortexes):
        if my_pos in vortexes:
            return ("bomb", 0)
        else:
            return ("bomb", Solution.crates_around_pos(my_pos, crates)*10)
    @staticmethod
    def crates_around_pos(pos, crates):
        next_to_me = [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]),
                (pos[0], pos[1]-1), (pos[0], pos[1]+1)]
        return len([c for c in crates if c in next_to_me])

    @staticmethod
    def position_score(pos, distance, crates, powerups, vortexes, maze):
        try:
            scores = (Solution.crates_around_pos(pos, crates)*10 +
                    1 if pos in powerups else 0)/len(distance[pos])
            return scores
        except Exception as e:
            #print("exception", distance[pos])
            return 0


def copypaste(my_pos, distance, crates, powerups, vortexes, players, maze):
    print("my_pos=", my_pos)
    print("distance=", distance)
    print("crates=", crates)
    print("powerups=", powerups)
    print("vortexes=", vortexes)
    print("players=", players)
    print("maze=", maze)
