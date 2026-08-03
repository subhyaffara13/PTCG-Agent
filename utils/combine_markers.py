import itertools

def combine_markers(cls):
    """
    pytest will honor markers as found on the class, but when
    markers are on multiple subclasses, only one appears. Use
    this decorator to combine those markers.
    """
    cls.pytestmark = [
        mark
        for base in itertools.chain([cls], cls.__bases__)
        for mark in getattr(base, 'pytestmark', [])
    ]
    return cls

