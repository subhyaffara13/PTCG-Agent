
def chain_from_iterable(iterable: Iterable[Iterable[_T]], /) -> Iterator[_T]:
    # previous version of this code was:
    #   return itertools.chain(*iterable)
    # If iterable is an infinite generator, this will lead to infinite recursion
    for it in iterable:
        yield from it

