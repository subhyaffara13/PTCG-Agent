from typing import Tuple

def _state_converter(itr: tSequence) -> Tuple | Range:
    """
    Helper function for converting list/tuple/set/Range/Tuple/FiniteSet
    to tuple/Range.
    """
    itr_ret: Tuple | Range

    if isinstance(itr, (Tuple, set, FiniteSet)):
        itr_ret = Tuple(*(sympify(i) if isinstance(i, str) else i for i in itr))

    elif isinstance(itr, (list, tuple)):
        # check if states are unique
        if len(set(itr)) != len(itr):
            raise ValueError('The state space must have unique elements.')
        itr_ret = Tuple(*(sympify(i) if isinstance(i, str) else i for i in itr))

    elif isinstance(itr, Range):
        # the only ordered set in SymPy I know of
        # try to convert to tuple
        try:
            itr_ret = Tuple(*(sympify(i) if isinstance(i, str) else i for i in itr))
        except (TypeError, ValueError):
            itr_ret = itr

    else:
        raise TypeError("%s is not an instance of list/tuple/set/Range/Tuple/FiniteSet." % (itr))
    return itr_ret

