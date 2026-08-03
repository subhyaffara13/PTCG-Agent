from typing import Callable

def iter_(fn_or_iterable, sentinel=_sentinel_missing, /):  # type: ignore[no-untyped-def]
    # Without a second argument, object must be a collection object which supports
    # the iterable (__iter__) or the sequence protocol (__getitem__ with an integer
    # starting at 0)
    if sentinel is _sentinel_missing:
        iterable = fn_or_iterable
        if hasattr(iterable, "__iter__"):
            iterator = iterable.__iter__()
            if hasattr(iterator, "__next__"):
                return iterator
            else:
                raise TypeError(f"'{type(iterator)}' object is not iterable")
        if hasattr(iterable, "__getitem__"):
            # Needs to be a new function to avoid iter becoming a generator
            def sequence_protocol(iterable):  # type: ignore[no-untyped-def]
                i = 0
                while True:
                    try:
                        yield iterable.__getitem__(i)
                        i += 1
                    except IndexError:
                        break

            return sequence_protocol(iterable)
        raise TypeError(f"'{type(iterable)}' object is not iterable")
    else:
        # If the second argument, sentinel, is given, then object must be a
        # callable object.
        fn = fn_or_iterable

        if not isinstance(fn, Callable):  # type: ignore[arg-type]
            raise TypeError("iter(v, w): v must be a callable")

        return _CallableIterator(fn, sentinel)

