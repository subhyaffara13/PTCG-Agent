
def __randomstate_ctor(bit_generator_name="MT19937",
                       bit_generator_ctor=__bit_generator_ctor):
    """
    Pickling helper function that returns a legacy RandomState-like object

    Parameters
    ----------
    bit_generator_name : str
        String containing the core BitGenerator's name
    bit_generator_ctor : callable, optional
        Callable function that takes bit_generator_name as its only argument
        and returns an instantized bit generator.

    Returns
    -------
    rs : RandomState
        Legacy RandomState using the named core BitGenerator
    """
    if isinstance(bit_generator_name, BitGenerator):
        return RandomState(bit_generator_name)
    return RandomState(bit_generator_ctor(bit_generator_name))

