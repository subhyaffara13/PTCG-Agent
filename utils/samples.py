
def samples(sound):
    """pygame.sndarray.samples(Sound): return array

    Reference Sound samples into an array.

    Creates a new array that directly references the samples in a Sound
    object. Modifying the array will change the Sound. The array will
    always be in the format returned from pygame.mixer.get_init().
    """

    return numpy.array(sound, copy=False)

