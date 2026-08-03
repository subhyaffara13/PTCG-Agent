from typing import Any

def mro(tp: type[Any]) -> tuple[type[Any], ...]:
    """Calculate the Method Resolution Order of bases using the C3 algorithm.

    See https://www.python.org/download/releases/2.3/mro/
    """
    # try to use the existing mro, for performance mainly
    # but also because it helps verify the implementation below
    if not is_typeddict(tp):
        try:
            return tp.__mro__
        except AttributeError:
            # GenericAlias and some other cases
            pass

    bases = get_bases(tp)
    return (tp,) + mro_for_bases(bases)

