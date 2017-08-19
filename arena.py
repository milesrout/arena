import random

class Cell:
    def render_char(self):
        return '#'

class EmptyCell(Cell):
    def render_char(self):
        return ' '

class Entity:
    def __init__(self, x, y):
        self.x, self.y = x, y
        objects[self.x][self.y].append(self)

    def render_char(self):
        return '?'

    def move(self, dx, dy):
        self.move_to(self.x + dx, self.y + dy)

    def move_to(self, x, y):
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            if len(objects[x][y]) == 0:
                if not len(objects[self.x][self.y]):
                    input()
                objects[self.x][self.y].remove(self)
                self.x = x
                self.y = y
                objects[self.x][self.y].append(self)

    def up(self):
        self.move(0, -1)

    def down(self):
        self.move(0, 1)

    def left(self):
        self.move(-1, 0)

    def right(self):
        self.move(1, 0)

    def attack_nearest(self):
        nearest = self.nearest()
        if len(nearest):
            entity = random.choice(random.choice(nearest))
            self.attack(entity)

    def nearest(self):
        offsets = [(-1,-1), (-1, 0), (-1, 1),
                   ( 0,-1),          ( 0, 1),
                   ( 1,-1), ( 1, 0), ( 1, 1)]
        indices = [(self.x + dx, self.y + dy)
                   for dx, dy in offsets
                   if 0 <= self.x + dx < WIDTH
                   if 0 <= self.y + dy < HEIGHT]
        return [objects[x][y]
                for (x, y) in indices
                if len(objects[x][y])]

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kills = 0

    def render_char(self):
        return '*'

    def attack(self, entity):
        self.kills += 1
        entity.destroy()

class Minion(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.status = 'alive'

    def render_char(self):
        return '.'

    def destroy(self):
        objects[self.x][self.y].remove(self)
        self.status = 'dead'

def render_world():
    print('+' + ('-' * WIDTH) + '+')
    for j in range(HEIGHT):
        print('|', end='')
        for i in range(WIDTH):
            if player in objects[i][j]:
                print(player.render_char(), end='')
            elif len(objects[i][j]):
                print(objects[i][j][0].render_char(), end='')
            else:
                print(base_world[i][j].render_char(), end='')
        print('|')
    print('+' + ('-' * WIDTH) + '+')

WIDTH, HEIGHT = 20, 10
PLAYERSTART_X, PLAYERSTART_Y = WIDTH // 2, HEIGHT // 2
NUM_MINIONS = 10

base_world = [[EmptyCell() for j in range(HEIGHT)] for i in range(WIDTH)]
objects    = [[list() for j in range(HEIGHT)] for i in range(WIDTH)]

player = Player(PLAYERSTART_X, PLAYERSTART_Y)

def random_location(except_from=None):
    if except_from is None:
        return random_location(set())

    if len(except_from) == WIDTH * HEIGHT:
        raise LogicError('Cannot create random location distinct from all possible locations')

    while True:
        pos = random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)
        if pos not in except_from:
            break

    return pos

def create_minions():
    minions = []
    used_locations = {(player.x, player.y)}
    for i in range(NUM_MINIONS):
        x, y = random_location(except_from=used_locations)
        used_locations.add((x, y))
        minions.append(Minion(x, y))
    return minions

minions = create_minions()

i = 0
def tick():
    global i, minions

    i += 1

    if all(m.status == 'dead' for m in minions):
        minions = create_minions()

    for m in minions:
        if m.status == 'alive' and random.random() < 0.25:
            random.choice((m.up, m.down, m.left, m.right))()
