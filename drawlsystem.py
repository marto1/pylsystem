from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.endpoints import connectProtocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import stdio
from time import sleep
import pygame, pygame.surfarray
from pygame.locals import *

alphabet=["A", "B", "-"]
axiom = "A"
rules = {"A":"B-B", 
         "B":"A-"}
rows = 10

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
        # self.sendLine(str(res))

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

def draw_it(line, y, surf):
    x = 0
    for char in line:
        if char == "A":
            x += 20
        elif char == "B":
            surf.set_at((x, y), (20, 200, 100))

def draw(surface, bg_surface):
    surface.blit(bg_surface, (0, 0))
    res = []
    fordraw = axiom
    for i in xrange(rows):
        res.append(fordraw)
        fordraw += loop(fordraw)
        draw_it(res[i], i*2+1, surface)

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
    ev.start(1.0 / 10)
    stdio.StandardIO(ChatboxProtocol())
    reactor.run()
        
if __name__ == '__main__':
    main()
    
