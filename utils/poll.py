
def poll():
    """poll() -> Event
    get an available event
    """
    _ft_init_check()
    return pygame.event.poll()

