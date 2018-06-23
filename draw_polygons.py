from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.endpoints import connectProtocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import stdio
from time import sleep
import pygame, pygame.surfarray
from pygame.locals import *
from math import sin, cos, degrees, radians

COL = (20, 200, 100)


def get_pos(length, x, y, angle):
    """ Compute the next coords by moving """  
    degrees = angle
    to_rad = radians(degrees)
    x_pos = round(cos(to_rad)*length+x)
    y_pos = round(sin(to_rad)*length+y)

    return (x_pos,y_pos)

def pendown(state):
    state[3] = True

def penup(state):
    state[3] = False

def forward(state, distance):
    new_x, new_y = get_pos(distance, state[0], state[1], state[4])
    if state[3]: # pendown
        pygame.draw.aaline(state[2], COL, (state[0], state[1]),
                           (new_x, new_y))
    state[0] = new_x
    state[1] = new_y

def backward(state, distance):
    right(state, 180)
    forward(state, distance)

def right(state, angle):
    r = state[4] + angle
    if r > 360 :
        state[4]= r - 360.0
    elif r < 0 :
        state[4]= r + 360.0  
    else :
        state[4] = r

def left(state, angle):
    r = state[4]- angle
    if r > 360 :
        state[4]= r - 360.0
    elif r < 0 :
        state[4] = r + 360.0  
    else :
        state[4] = r

# axiom = "PFRFRFRF" #4

# axiom = "PFRFFRFRFF" #6

# axiom = "PFRFFFRFRFFF" #8.1
# axiom = "PFFRFFRFFRFF" #8.2
# axiom = "PFRFLFRFRFFRFF" #8.3

# axiom = "PFRFFFFRFRFFFF" #10.1
# axiom = "PFFFRFFRFFFRFF" #10.2
# axiom = "PFFFRFRFLFRFFRFF" #10.3
# axiom = "PFFFRFRFLFRFRFLFRF" #10.4
# axiom = "PFFFRFRFFLFRFRFF" #10.5
axiom = "PFRFFRFLFRFRFFRFLF" #10.6

rules = {}
# rules = {"R": "LFFF", "F": "FFRB"}


operations = {
    "P": lambda x: pendown(x),
    "U": lambda x: penup(x),
    "R": lambda x: right(x, 90),
    "L": lambda x: left(x, 90),
    "F": lambda x: forward(x, 90),
    "B": lambda x: backward(x, 90),
}

generations = 9

class ChatboxProtocol(LineReceiver):
    """
    Protocol for making requests that also responds in the default
    way.
    """

    delimiter = '\n'

    def __init__(self):
        pass

    def connectionMade(self):
        self.sendLine("ready.")

    def lineReceived(self, line):
        # Ignore blank lines
        if not line: return
        exec(line, globals())

    def connectionLost(self, reason):
        # stop the reactor, only
        # because this is meant to be run in Stdio.
        reactor.stop()


def loop(axiom):
    res = ""
    for letter in axiom:
        if letter in rules:
            res += rules[letter]
    return res

def draw_it(line, surf):
    #state   x  y  bg    pen   angle
    state = [400, 150, surf, False, 0.0]
    for char in line:
        if char in operations:
            operations[char](state)

def draw(surface, bg_surface):
    global axiom
    surface.blit(bg_surface, (0, 0))
    fordraw = axiom
    for i in xrange(generations):
        fordraw += loop(fordraw)
    draw_it(fordraw, surface)
    pygame.display.flip()

# just draw axiom
# def main():
#     pygame.init()
#     screen_width, screen_height = (1024, 600)
#     size = (screen_width,screen_height)
#     clock = pygame.time.Clock()
#     pygame.display.set_caption("Generate polygons")
#     surface = pygame.display.set_mode(size)
#     bg_surface = pygame.Surface(size, pygame.SRCALPHA)
#     bg_surface.fill((0, 0,0))
#     ev = LoopingCall(draw, surface, bg_surface)
#     ev.start(1.0 / 2)
#     stdio.StandardIO(ChatboxProtocol())
#     reactor.run()

# randomize polygon creation
# from random import choice, randint

# def randomize():
#     global axiom
#     alpha = ["F"]
#     for i in range(9):
#         alpha.append(choice(["", "R", "L"]))
#         alpha.append("F")
#     alpha = "".join(alpha)
#     axiom = "P{}".format(alpha)
#     print axiom


# def main():
#     pygame.init()
#     screen_width, screen_height = (1024, 600)
#     size = (screen_width,screen_height)
#     clock = pygame.time.Clock()
#     pygame.display.set_caption("L-system generate")
#     surface = pygame.display.set_mode(size)
#     bg_surface = pygame.Surface(size, pygame.SRCALPHA)
#     bg_surface.fill((0, 0,0))
#     ev = LoopingCall(draw, surface, bg_surface)
#     ev.start(1.0 / 2)
#     ev2 = LoopingCall(randomize)
#     ev2.start(0.3)
#     stdio.StandardIO(ChatboxProtocol())
#     reactor.run()

# generate all
from itertools import product

def filter_useless_slots(x):
    coord = [1,0] #current coordinates, first step is always F 
    direction = 0 #of the vector
    history = [[1,0]] #all visited points without 0,0
    # directions: 0 - right
    #             1 - down
    #             2 - left
    #             3 - up
    s = "{}F".format("F".join(x)).replace(" ", "")
    # print s
    for slot in s:
        # print coord, slot
        if slot == "F":
            if direction == 0:
                coord[0] += 1
            if direction == 2:
                coord[0] -= 1
            if direction == 3:
                coord[1] += 1
            if direction == 1:
                coord[1] -= 1
            if coord in history: #eliminate repeating coords
                return False
            history.append(list(coord))
        if slot == "R": #change direction
            if direction != 3:
                direction +=1
            else:
                direction = 0
        if slot == "L": #change direction
            if direction != 0:
                direction -= 1
            else:
                direction = 3
    if coord[0] == 0 and coord[1] == 0:
        return True
    return False

slot_counter = 0
slots = list(product(" RL", repeat=11)) #10
slots = filter(filter_useless_slots, slots)
print "slots:", len(slots)

#yield doesnt work :/
def call_new():
    global axiom, slot_counter, slots
    if slot_counter == len(slots):
        return
    axiom = "PF{}F".format("F".join(slots[slot_counter]))
    # print axiom
    slot_counter += 1


def main():
    pygame.init()
    screen_width, screen_height = (1024, 600)
    size = (screen_width,screen_height)
    clock = pygame.time.Clock()
    pygame.display.set_caption("L-system generate")
    surface = pygame.display.set_mode(size)
    bg_surface = pygame.Surface(size, pygame.SRCALPHA)
    bg_surface.fill((0, 0,0))
    ev = LoopingCall(draw, surface, bg_surface)
    ev.start(1.0 / 10)
    ev2 = LoopingCall(call_new)
    ev2.start(0.1)
    stdio.StandardIO(ChatboxProtocol())
    reactor.run()


if __name__ == '__main__':
    main()
    
