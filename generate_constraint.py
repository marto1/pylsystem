"""
Using randomized patterns try to satisfy constraint.

"""


from drawlsystem import *
from random import choice, randint
import drawlsystem

def randomize():
    alpha = ["L", "F", "R", "B"]
    n = randint(1, 12)
    drawlsystem.axiom = "P{}".format("".join([choice(alpha) for i in xrange(n)]))
    print drawlsystem.axiom
    
def generate():
    pygame.init()
    screen_width, screen_height = (1024, 600)
    size = (screen_width,screen_height)
    clock = pygame.time.Clock()
    pygame.display.set_caption("L-system generate")
    surface = pygame.display.set_mode(size)
    bg_surface = pygame.Surface(size, pygame.SRCALPHA)
    bg_surface.fill((0, 0,0))
    ev = LoopingCall(draw, surface, bg_surface)
    ev.start(1.0 / 2)
    ev2 = LoopingCall(randomize)
    ev2.start(2.0)
    stdio.StandardIO(ChatboxProtocol())
    reactor.run()

generate()
