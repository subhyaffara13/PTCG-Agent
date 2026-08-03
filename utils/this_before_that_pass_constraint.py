from typing import Callable

def this_before_that_pass_constraint(this: Callable, that: Callable):
    """
    Defines a partial order ('depends on' function) where `this` must occur
    before `that`.
    """

    def depends_on(a: Callable, b: Callable):
        return a != that or b != this

    return depends_on


def this_before_that_pass_constraint(this: Callable, that: Callable) -> Callable:
    """
    Defines a partial order ('depends on' function) where ``this`` must occur
    before ``that``.

    For example, the following pass list and constraint list would be invalid::

        passes = [pass_b, pass_a]

        constraints = [this_before_that_pass_constraint(pass_a, pass_b)]

    Args:
        this (Callable): pass which should occur first
        that (Callable): pass which should occur later

    Returns:
        depends_on (Callable[[Object, Object], bool])
    """

    def depends_on(a: Callable, b: Callable):
        return a != that or b != this

    return depends_on

