from itertools import product
from collections import namedtuple
from pprint import pprint

class State:
    def __init__(self):
        self.avatar = None
        self.powerup = 1
        self.crate = 5
        self.player = 20
        self.immolation = -10
        self.tick = 0
        self.maze = {}
        self.powerups = []
        self.vortexes = []
        self.crates = []
        self.power = {}

    def init_map(self, maze_width, maze_height, walls):
        """
        :return type: dict[tuple(int, int)] = None
        """
        maze = {xy: None for xy in product(
                     range(maze_width), range(maze_height))}

        for xy in (self.to_pos(xy) for xy in walls):
            del self.maze[xy]
        self.maze = maze
        return maze

    def update_players(self, str_players):
        player_to_xy = {player: to_pos(str_xy)
                for player, str_xy in str_players.items()}
        self.players.append(player_to_xy)

    def update_vortexes(self, vortexes):
        self.vortexes.append([self.to_pos(v) for v in vortexes])

    def update_powerups(self, str_powerups):
        powerups = [self.to_pos(p) for p in str_powerups]
        for p, xy in self.players[-1].items():
            if xy in powerups:
                self.power[-1][p] += 1

    def to_pos(self, str_pos):
        x, y = str_pos.replace("(","").replace(")","").split(",")
        return int(x), int(y)

    def init_players(self, your_avatar, players):
        self.avatar = your_avatar
        self.players = [players]
        self.power = [{p: 1 for p in players.keys()}]
        self.power[-1][self.avatar] = 1

    @property
    def my_pos(self):
        return self.players[-1][self.avatar]

    @property
    def my_power(self):
        return self.power[-1][self.avatar]

    @property
    def enemies(self):
        return [pos for player, pos in self.players[-1].items()
                if player != self.avatar]


def calculate_distance(state, pos):
    """
    :type state: class state
    :type blocked_pos: Tuple(int, int), positions one cannot move to
    """
    try:
        blocked_pos = state.crates[-1] + state.enemies
    except IndexError:
        blocked_pos = state.enemies
    distance = state.maze.copy()
    queue = [(state.my_pos, [])]
    while queue:
        pos, way = queue.pop(0)
        if distance[pos] is None:
            distance[pos] = [pos] + way
            new_way = [pos] + way
            neig = ((pos, new_way.copy()) for pos in
                    neighbours(state,pos) if distance[pos] is None and pos not in blocked_pos)
            queue.extend(neig)
    return distance

def neighbours(state, pos):
    """
    :type pos: tuple(int, int)
    :type state: class State
    """
    all_neighbours = [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]),
            (pos[0], pos[1]-1), (pos[0], pos[1]+1)]
    valid_neighbours = [n for n in all_neighbours if n in state.maze]
    return valid_neighbours

class Solution:
    def __init__(self, api):
        self.api = api
        self.powerup = 1
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
        if action == (0,0):
            copypaste(my_pos, distance, crates, powerups, vortexes, players, self.maze)
        print("best action: ", action, score)
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
            scores = (Solution.eval_bomb(pos, crates, vortexes)[1]*0.8 +
                    (1 if pos in powerups else 0))/len(distance[pos])
            return scores
        except TypeError as e:
            return 0


def copypaste(my_pos, distance, crates, powerups, vortexes, players, maze):
    print("my_pos=", my_pos)
    print("distance=", distance)
    print("crates=", crates)
    print("powerups=", powerups)
    print("vortexes=", vortexes)
    print("players=", players)
    print("maze=", maze)
