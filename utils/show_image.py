
def show_image(s, images=[]):
    # pygame.display.init()
    size = s.get_rect()[2:]
    screen = pygame.display.set_mode(size)
    screen.blit(s, (0, 0))
    pygame.display.flip()
    pygame.event.pump()
    going = True
    idx = 0
    while going:
        events = pygame.event.get()
        for e in events:
            if e.type == QUIT:
                going = False
            if e.type == KEYDOWN:
                if e.key in [K_s, K_a]:
                    if e.key == K_s:
                        idx += 1
                    if e.key == K_a:
                        idx -= 1
                    s = images[idx]
                    screen.blit(s, (0, 0))
                    pygame.display.flip()
                    pygame.event.pump()
                elif e.key in [K_ESCAPE]:
                    going = False
    pygame.display.quit()
    pygame.display.init()

