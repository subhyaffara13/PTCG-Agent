
def make_sound(array):
    """pygame.sndarray.make_sound(array): return Sound

    Convert an array into a Sound object.

    Create a new playable Sound object from an array. The mixer module
    must be initialized and the array format must be similar to the mixer
    audio format.
    """

    return mixer.Sound(array=array)

