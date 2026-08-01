
def __generator_ctor(bit_generator_name="MT19937",
                     bit_generator_ctor=__bit_generator_ctor):
    """
    Pickling helper function that returns a Generator object

    Parameters
    ----------
    bit_generator_name : str or BitGenerator
        String containing the core BitGenerator's name or a
        BitGenerator instance
    bit_generator_ctor : callable, optional
        Callable function that takes bit_generator_name as its only argument
        and returns an instantized bit generator.

    Returns
    -------
    rg : Generator
        Generator using the named core BitGenerator
    """
    if isinstance(bit_generator_name, BitGenerator):
        return Generator(bit_generator_name)
    # Legacy path that uses a bit generator name and ctor
    return Generator(bit_generator_ctor(bit_generator_name))

