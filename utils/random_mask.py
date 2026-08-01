
def random_mask(size=(100, 100)):
    """random_mask(size=(100,100)): return Mask
    Create a mask of the given size, with roughly half the bits set at random."""
    m = pygame.Mask(size)
    for i in range(size[0] * size[1] // 2):
        x, y = random.randint(0, size[0] - 1), random.randint(0, size[1] - 1)
        m.set_at((x, y))
    return m

