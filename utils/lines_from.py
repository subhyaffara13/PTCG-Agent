
def lines_from(input):
    """
    Generate lines from a :class:`importlib.resources.abc.Traversable` path.

    >>> lines = lines_from(files(__name__).joinpath('Lorem ipsum.txt'))
    >>> next(lines)
    'Lorem ipsum...'
    >>> next(lines)
    'Curabitur pretium...'
    """
    with input.open(encoding='utf-8') as stream:
        yield from stream

