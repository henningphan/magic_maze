from itertools import product
from collections import namedtuple
from pprint import pprint

class State:
    def __init__(self):
        self.avatar = None
        self.tick = 0
        self.powerup = 1
        self.crate = 5
        self.player = 20
        self.immolation = -10
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
            del maze[xy]
        self.maze = maze
        return maze

    def update_players(self, str_players):
        player_to_xy = {player: self.to_pos(str_xy)
                for player, str_xy in str_players.items()}
        self.players.append(player_to_xy)

    def update_vortexes(self, str_vortexes):
        self.vortexes.append([self.to_pos(v) for v in str_vortexes])

    def update_powerups(self, str_powerups):
        powerups = [self.to_pos(p) for p in str_powerups]
        for p, xy in self.players[-1].items():
            if xy in powerups:
                self.power[-1][p] += 1

    def update_crates(self, str_crates):
        self.crates.append([self.to_pos(c) for c in str_crates])

    def to_pos(self, str_pos):
        x, y = str_pos.replace("(","").replace(")","").split(",")
        return int(x), int(y)

    def init_players(self, players):
        self.players = [{p: self.to_pos(xy) for p,xy in players.items()}]
        self.power = [{p: 1 for p in players.keys()}]

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
        self.state = State()
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
        self.state.avatar = your_avatar
        self.state.init_map(maze_width, maze_height, walls)

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
        print("avatar:", self.state.avatar)
        if self.tick == 0:
            self.state.init_players(players)
        self.tick += 1
        self.state.update_players(players)
        self.state.update_powerups(powerups)
        self.state.update_crates(crates)
        self.state.update_vortexes(vortexes)


        action, score = next_action(self.state)
        print("best action: ", action, score)
        if action == "bomb":
            self.api.magical_explosion()
        else:
            pos = action
            self.api.move(*pos)

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

def next_action(state):
    bomb_score = eval_bomb(state)
    distance = calculate_distance(state, state.my_pos)
    pos_score = [(pos, position_score(state, pos, distance)) for pos in state.maze.copy().keys()]
    scores = pos_score + [bomb_score]
    scores.sort(key=lambda tup: tup[1], reverse=True)
    if scores[0][0] == "bomb":
        return scores[0]
    else:
        return (scores[0][0], Solution.move_to(distance, scores[0][0]))

def eval_bomb(state):
    if state.my_pos in state.vortexes[-1]:
        return ("bomb", 0)
    else:
        return ("bomb", crates_around_pos(state.my_pos, state.crates[-1])*state.crate)

def crates_around_pos(pos, crates):
    next_to_me = [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]),
            (pos[0], pos[1]-1), (pos[0], pos[1]+1)]
    return len([c for c in crates if c in next_to_me])

def position_score(state, distance, pos):
    try:
        scores = (eval_bomb(pos, state.crates[-1], state.vortexes[-1])[1]*0.8 +
                (1 if pos in powerups else 0))/len(distance[pos])
        return scores
    except TypeError as e:
        return 0
