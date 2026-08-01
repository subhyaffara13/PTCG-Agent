
def _check_fails(cls, other):
    try:
        if sys._getframe(1).f_globals['__name__'] not in ['abc', 'functools', 'typing']:
            # Typed dicts are only for static structural subtyping.
            raise TypeError('TypedDict does not support instance and class checks')
    except (AttributeError, ValueError):
        pass
    return False

