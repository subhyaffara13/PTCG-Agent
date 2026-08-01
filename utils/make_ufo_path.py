
def makeUFOPath(path: PathStr) -> str:
    """
    Return a .ufo pathname.

    >>> makeUFOPath("directory/something.ext") == (
    ... 	os.path.join('directory', 'something.ufo'))
    True
    >>> makeUFOPath("directory/something.another.thing.ext") == (
    ... 	os.path.join('directory', 'something.another.thing.ufo'))
    True
    """
    dir, name = os.path.split(path)
    name = ".".join([".".join(name.split(".")[:-1]), "ufo"])
    return os.path.join(dir, name)

