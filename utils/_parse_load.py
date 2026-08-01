
def _parse_load(load):
    """Helper function to parse loads and convert tuples to load objects."""
    if isinstance(load, LoadBase):
        return load
    elif isinstance(load, tuple):
        if len(load) != 2:
            raise ValueError(f'Load {load} should have a length of 2.')
        if isinstance(load[0], Point):
            return Force(load[0], load[1])
        elif isinstance(load[0], ReferenceFrame):
            return Torque(load[0], load[1])
        else:
            raise ValueError(f'Load not recognized. The load location {load[0]}'
                             f' should either be a Point or a ReferenceFrame.')
    raise TypeError(f'Load type {type(load)} not recognized as a load. It '
                    f'should be a Force, Torque or tuple.')

