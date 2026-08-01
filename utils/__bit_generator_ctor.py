
def __bit_generator_ctor(bit_generator: str | type[BitGenerator] = 'MT19937'):
    """
    Pickling helper function that returns a bit generator object

    Parameters
    ----------
    bit_generator : type[BitGenerator] or str
        BitGenerator class or string containing the name of the BitGenerator

    Returns
    -------
    BitGenerator
        BitGenerator instance
    """
    if isinstance(bit_generator, type):
        bit_gen_class = bit_generator
    elif bit_generator in BitGenerators:
        bit_gen_class = BitGenerators[bit_generator]
    else:
        raise ValueError(
            str(bit_generator) + ' is not a known BitGenerator module.'
        )

    return bit_gen_class()

