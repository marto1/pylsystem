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


# rules = {"P":"PFF", 
#          "F":"FRF",
#          "R": "RF",
# }

# region divide
# rules = {"P":"PFF", "F":"FRF", "R": "RF",}
# rules = {"P":"PFF", "F":"FFR", "R": "",}
# rules = {"F":"FFRRF", "R": "FFFFF",}

# rules = {"F":"FFRRBBF", "R": "FFFFF",} #barbed wire
# rules = {"F":"FFRBBBF", "R": "FFFRF"} #stars
# rules = {"F":"FRBBBFF", "R": "FFRRF"} #more stars
# RRRRRRRRFFFFRRRRRRRRRFFFFRRRRRRRRRFFFF


# cool circles
#state = [400, 400, surf, False, 0.0]
# axiom = "PFFFR"
# rules = {"R": "FRFFRRRFL", "F": "FLFR"}
# "R": lambda x: right(x, 10),
# "L": lambda x: left(x, 10),

# cool circles
#state = [400, 400, surf, False, 0.0]
# axiom = "PFFFR"
# rules = {"R": "FRFFRRRFL", "F": "FLFR"}
# "R": lambda x: right(x, 10),
# "L": lambda x: left(x, 10),

# cool matrix like generation
# "R": lambda x: right(x, 90),
# "L": lambda x: left(x, 90),

# squares
# rules = {"R": "FRFFFRF", "F": "FRF"}
# "R": lambda x: right(x, 90),
# "L": lambda x: left(x, 90),

# parallelepiped
# "R": lambda x: right(x, 60),
# "L": lambda x: left(x, 60),
# axiom = "PFFR"
# rules = {"R": "FRF", "F": "FFR"}

#triangles
#axiom = "PFFR"
#rules = {"R": "FRF", "F": "FFRB"}
# "R": lambda x: right(x, 60),
# "L": lambda x: left(x, 60),

#pythagorean tiling
# axiom = "PFFR"
# rules = {"R": "FRF", "F": "FFRB"}
# "R": lambda x: right(x, 90),
# "L": lambda x: left(x, 90),

axiom = "PFFR"
rules = {"R": "FRF", "F": "FFRB"}

operations = {
    "P": lambda x: pendown(x),
    "U": lambda x: penup(x),
    "R": lambda x: right(x, 90),
    "L": lambda x: left(x, 90),
    "F": lambda x: forward(x, 20),
    "B": lambda x: backward(x, 20),
}

generations = 5

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
    state = [800, 150, surf, False, 0.0]
    for char in line:
        operations[char](state)

def draw(surface, bg_surface):
    surface.blit(bg_surface, (0, 0))
    fordraw = axiom
    for i in xrange(generations):
        fordraw += loop(fordraw)
    draw_it(fordraw, surface)
    pygame.display.flip()
    
def main():
    pygame.init()
    screen_width, screen_height = (1024, 600)
    size = (screen_width,screen_height)
    clock = pygame.time.Clock()
    pygame.display.set_caption("L-system draw")
    surface = pygame.display.set_mode(size)
    bg_surface = pygame.Surface(size, pygame.SRCALPHA)
    bg_surface.fill((0, 0,0))
    ev = LoopingCall(draw, surface, bg_surface)
    ev.start(1.0 / 2)
    stdio.StandardIO(ChatboxProtocol())
    reactor.run()
    # draw(surface, bg_surface)
        
if __name__ == '__main__':
    main()
    
