from itertools import product, groupby, chain
from collections import namedtuple, defaultdict
from pprint import pprint
from copy import deepcopy

Vort = namedtuple("Vort", ["pos", "power", "time"])
Action = namedtuple("Action", ["name", "my_pos", "dst", "score"])
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
        self.players = []
        self.vortexes = []
        self.crates = []
        self.power = defaultdict(lambda: 1)
        self.phantoms = []
        self.phantom_cache = set()

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

    def update_all(self, crates, powerups, vortexes, players):
        self.update_players(players)
        self.update_vortexes(vortexes)
        self.update_crates(crates)
        self.update_powerups(powerups)

    def update_players(self, str_players):
        player_to_xy = {player: self.to_pos(str_xy)
                for player, str_xy in str_players.items()}
        self.players = player_to_xy
        self.phantoms.append(set(self.enemies))
        self.phantom_cache = set(chain(*self.phantoms[-4:]))

    def update_vortexes(self, str_vortexes):
        def get_power(xy):
            player = [player for player, pos in self.players.items() if xy == pos][0]
            power = self.power[player]
            return power
        def get_previous():
            try:
                return self.vortexes
            except Exception:
                return []
        incoming_vort = [self.to_pos(str_pos) for str_pos in str_vortexes]
        previous = [v._replace(time=v.time-1) for v in get_previous()
                        if v.time >= 0 and v.pos in incoming_vort]
        new = [Vort(pos, get_power(pos), 6) for pos in incoming_vort
                if pos not in set(v.pos for v in previous)]
        self.vortexes = previous+new

    def update_powerups(self, str_powerups):
        powerups = [self.to_pos(p) for p in str_powerups]
        for p, xy in self.players.items():
            if xy in powerups:
                self.power[p] += 1
        self.powerups = powerups

    def update_crates(self, str_crates):
        self.crates = [self.to_pos(c) for c in str_crates]

    def to_pos(self, str_pos):
        if isinstance(str_pos, tuple):
            return str_pos
        x, y = str_pos.replace("(","").replace(")","").split(",")
        return int(x), int(y)

    @property
    def my_pos(self):
        return self.players[self.avatar]

    @property
    def my_power(self):
        return self.power[self.avatar]

    @property
    def enemies(self):
        return [pos for player, pos in self.players.items()
                if player != self.avatar]

    def dump(self):
        copy_dict = self.__dict__.copy()
        copy_dict["power"] = dict(self.power)
        print(copy_dict)

    def dumpp(self):
        copy_dict = self.__dict__.copy()
        copy_dict["power"] = dict(self.power)
        pprint(copy_dict)

def calculate_future(state, depth=4):
    maze = state.maze
    vortexes = state.vortexes
    crates = state.crates


def calculate_distance(state, pos):
    """
    :type state: class state
    :type blocked_pos: Tuple(int, int), positions one cannot move to
    """
    try:
        blocked_pos = state.crates + state.enemies
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

def next_action(state):
    """
    returns tuple(action, score)
    """
    def get_penalty(penalty_table, distance, pos):
        try:
            return penalty_table[distance[pos][-2]]
        except:
            return penalty_table[distance[pos][-1]]


    bomb_crates = calc_bomb_crates(state, depth=7)
    penalty_table = create_action_penalty_lookup(state)
    bomb_score = Action("bomb",
            state.my_pos,
            state.my_pos,
            eval_bomb(state, state.my_pos, bomb_crates)-penalty_table["bomb"]*20)
    distance = calculate_distance(state, state.my_pos)
    pos_score = [Action(move_to(distance, pos),
        state.my_pos,
        pos,
        position_score(state, distance, pos, bomb_crates)- get_penalty(penalty_table, distance,pos)*20)
                    for pos, dis in distance.items()
                        if dis is not None]
    actions = pos_score + [bomb_score]
    actions.sort(key=lambda action: action.score, reverse=True)
    return actions

def create_action_penalty_lookup(state):
    """
    Returns dict with action mapped to penalty
    """
    action_death = {}
    state2 = deepcopy(state)
    players = state2.players.copy()
    heatmap, vortexes = create_heatmap(state2)
    vortexes = [str(v.pos) for v in vortexes]
    vortexes.append(str(state2.my_pos)) # add my own bomb
    crates = [str(c) for c in state2.crates if c not in heatmap]
    state2.update_all(crates, [], vortexes, players)
    action_death["bomb"] = is_dying(state2, depth=3)
    for pos in get_valid_ways(state, state.my_pos):
        if len(state.vortexes) == 0:
            action_death[pos] = 0
            continue
        state2 = deepcopy(state)
        players = state2.players.copy()
        players[state2.avatar] = pos
        heatmap, vortexes = create_heatmap(state2)
        vortexes = [str(v.pos) for v in vortexes]
        crates = [str(c) for c in state2.crates if c not in heatmap]
        state2.update_all(crates, [], vortexes, players)
        action_death[pos] = is_dying(state2, depth=3)
    return action_death

def get_valid_ways(state, pos):
    """
    Returns list of positions an avatar can move to
    """
    all_moves = [pos, (pos[0]-1, pos[1]), (pos[0]+1, pos[1]),
            (pos[0], pos[1]-1), (pos[0], pos[1]+1)]
    heatmap, _ = create_heatmap(state)
    blocked = [c for c in state.crates if c not in heatmap]
    return [m for m in all_moves if m in state.maze and m not in blocked]

def is_dying(state, depth=3):
    """
    Returns 1 if I die by my actions else returns 0
    """
    if len(state.vortexes) == 0:
        return 0
    heatmap, vortexes = create_heatmap(state)
    if state.my_pos in heatmap:
        return 1

    if depth == 0:
        return 1 if state.my_pos in heatmap else 0

    distance = calculate_distance(state, state.my_pos)
    for way in get_valid_ways(state, state.my_pos):
        state2 = deepcopy(state)
        players = state2.players.copy()
        players[state2.avatar] = way
        players = {p: str(pos) for p, pos in players.items()}
        heatmap, vortexes = create_heatmap(state2)
        vortexes = [str(v.pos) for v in vortexes]
        crates = [str(c) for c in state2.crates if c not in heatmap]
        state2.update_all(crates, [], vortexes, players)
        status = is_dying(state2, depth=depth-1)
        if status == 0:
            return 0
    return 1


def eval_bomb(state, pos, bomb_crates):
    if pos in {v.pos for v in state.vortexes}:
        return 0
    else:
        bm = bomb_map(state, Vort(pos, state.my_power, 0))
        crates_destroyed = len([p for p in bm if p in bomb_crates[6][1]])
        phantoms_destroyed = len([p for p in bm if p in state.phantom_cache])
        return crates_destroyed*state.crate + phantoms_destroyed*0.2

def crates_around_pos(pos, crates):
    next_to_me = [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]),
            (pos[0], pos[1]-1), (pos[0], pos[1]+1)]
    return len([c for c in crates if c in next_to_me])

def position_score(state, distance, pos, bomb_crates):
    scores = (eval_bomb(state, pos, bomb_crates)*0.8 +
            (1 if pos in state.powerups and state.my_pos != pos else 0))/len(distance[pos])
    return scores

def survive(state):
    pass

def create_heatmap(state):
    """
    returns a map of positions which are deadly
    and a list of vortexes which hasnt detonated yet
    """
    vortexes = state.vortexes
    vortexes.sort(key=lambda x: x.time)
    heatmap = set()
    untouched = {v.pos: v for v in vortexes}
    queue = [v for v in vortexes if v.time == 0]
    while queue:
        vortex = queue.pop(0)
        try:
            del untouched[vortex.pos]
        except:
            pass

        for pos in bomb_map(state, vortex):
            heatmap.add(pos)
            if pos in untouched:
                queue.append(untouched[pos])
    return heatmap, untouched.values()

def calc_bomb_crates(state, depth=7):
    """
    Returns list[tuple(heatmap, crates)]
    heatmap: set of positions where an explosion ocurred
    crates: set of all available crates
    """
    all_vort = set(state.vortexes)
    detonated = set()
    history = []
    all_crates = set(state.crates)
    exploded_crates = set()
    for d in range(depth):
        heatmap = set()
        queue = [v for v in all_vort
                 if v.time == d and v not in detonated]
        detonated.update(queue)
        while queue:
            v = queue.pop()
            bm = bomb_map(state, v)
            heatmap.update(bm)
            diff_vortexes = [v for v in all_vort.difference(detonated)
                    if v.pos in bm]
            detonated.update(diff_vortexes)
        diff_crates = {c for c in all_crates.difference(exploded_crates)
                       if c in heatmap}

        exploded_crates.update(diff_crates)
        history.append((heatmap, all_crates.difference(exploded_crates)))
    return history



def bomb_map(state, vort):
    """
    Returns list of positions that will explode
    """
    pos = vort.pos
    bombed_pos = [pos]
    for xy in ((x, pos[1]) for x in range(pos[0]+1, pos[0]+vort.power+1)):
        if xy not in state.maze:
            break
        bombed_pos.append(xy)
    for xy in ((x, pos[1]) for x in range(pos[0]-1, pos[0]-vort.power-1, -1)):
        if xy not in state.maze:
            break
        bombed_pos.append(xy)
    for xy in ((pos[0], y) for y in range(pos[1]+1, pos[1]+vort.power+1)):
        if xy not in state.maze:
            break
        bombed_pos.append(xy)
    for xy in ((pos[0], y) for y in range(pos[1]-1, pos[1]-vort.power-1, -1)):
        if xy not in state.maze:
            break
        bombed_pos.append(xy)
    return bombed_pos


def detonate_all_map(state):
    bm = set()
    for v in state.vortexes:
        bm.update(bomb_map(state, v))
    return bm


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
        self.tick += 1
        self.state.update_all(crates, powerups, vortexes, players)
        self.state.dump()

        actions = next_action(self.state)
        best_action = actions[0]
        print("avatar:", self.state.avatar)
        print("my_pos:", self.state.my_pos)
        print("best action: ", best_action)
        if best_action.score < 0:
            print(actions)
        if best_action.name == "bomb":
            self.api.magical_explosion()
        else:
            self.api.move(*best_action.name)

