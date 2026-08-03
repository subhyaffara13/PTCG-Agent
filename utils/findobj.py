from typing import Callable

def findobj(
    o: Artist | None = None,
    match: Callable[[Artist], bool] | type[Artist] | None = None,
    include_self: bool = True
) -> list[Artist]:
    if o is None:
        o = gcf()
    return o.findobj(match, include_self=include_self)

