from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.endpoints import connectProtocol
from time import sleep
import pygame, pygame.surfarray
from pygame.locals import *

alphabet=["A", "B", "-"]
axiom = "A"
rules = {"A":"B-B", 
         "B":"A-"}

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

def draw(surface):
    res = []
    fordraw = axiom
    for i in xrange(10):
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
    ev = LoopingCall(draw, surface, )
    ev.start(1.0 / 60)
    reactor.run()
        
if __name__ == '__main__':
    main()
    
