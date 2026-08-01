
def _solve_undetermined(g, symbols, flags):
    """solve helper to return a list with one dict (solution) else None

    A direct call to solve_undetermined_coeffs is more flexible and
    can return both multiple solutions and handle more than one independent
    variable. Here, we have to be more cautious to keep from solving
    something that does not look like an undetermined coeffs system --
    to minimize the surprise factor since singularities that cancel are not
    prohibited in solve_undetermined_coeffs.
    """
    if g.free_symbols - set(symbols):
        sol = solve_undetermined_coeffs(g, symbols, **dict(flags, dict=True, set=None))
        if len(sol) == 1:
            return sol

