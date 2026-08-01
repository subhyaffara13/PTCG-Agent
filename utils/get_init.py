
def get_init():
    """get_init() -> bool
    returns True if the fastevent module is currently initialized
    """
    return _ft_init


def get_init():
    """get_init() -> bool
    true if the font module is initialized"""

    return _get_init()


def get_init():
    """returns True if the midi module is currently initialized
    pygame.midi.get_init(): return bool

    Returns True if the pygame.midi module is currently initialized.

    New in pygame 1.9.5.
    """
    return _module_init()

