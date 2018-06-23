
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

# if ((direction >> 0)  & 0x01) == ((direction >> 1)  & 0x01):
#     coord[direction % 2] += 1
# else:
#     coord[direction % 2] -= 1
