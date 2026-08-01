
def sound_from_pos(sound, start_pos, samples_per_second=None, inplace=1):
    """returns a sound which begins at the start_pos.
    start_pos - in seconds from the beginning.
    samples_per_second -
    """

    # see if we want to reuse the sound data or not.
    if inplace:
        a1 = pg.sndarray.samples(sound)
    else:
        a1 = pg.sndarray.array(sound)

    # see if samples per second has been given.  If not, query the pg.mixer.
    #   eg. it might be set to 22050
    if samples_per_second is None:
        samples_per_second = pg.mixer.get_init()[0]

    # figure out the start position in terms of samples.
    start_pos_in_samples = int(start_pos * samples_per_second)

    # cut the beginning off the sound at the start position.
    a2 = a1[start_pos_in_samples:]

    # make the Sound instance from the array.
    sound2 = pg.sndarray.make_sound(a2)

    return sound2

