
def _remove_duplicate_solutions(solutions: list[dict[Expr, Expr]]
                                ) -> list[dict[Expr, Expr]]:
    """Remove duplicates from a list of dicts"""
    solutions_set = set()
    solutions_new = []

    for sol in solutions:
        solset = frozenset(sol.items())
        if solset not in solutions_set:
            solutions_new.append(sol)
            solutions_set.add(solset)

    return solutions_new

