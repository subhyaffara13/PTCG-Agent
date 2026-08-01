
def refactor_levels(
    level: Level | list[Level] | None,
    obj: Index,
) -> list[int]:
    """
    Returns a consistent levels arg for use in ``hide_index`` or ``hide_columns``.

    Parameters
    ----------
    level : int, str, list
        Original ``level`` arg supplied to above methods.
    obj:
        Either ``self.index`` or ``self.columns``

    Returns
    -------
    list : refactored arg with a list of levels to hide
    """
    if level is None:
        levels_: list[int] = list(range(obj.nlevels))
    elif isinstance(level, int):
        levels_ = [level]
    elif isinstance(level, str):
        levels_ = [obj._get_level_number(level)]
    elif isinstance(level, list):
        levels_ = [
            obj._get_level_number(lev) if not isinstance(lev, int) else lev
            for lev in level
        ]
    else:
        raise ValueError("`level` must be of type `int`, `str` or list of such")
    return levels_

