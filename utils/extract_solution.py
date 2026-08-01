
def extract_solution(set_sol, n=10):
    """Extract numerical solutions from a set solution (computed by solveset,
    linsolve, nonlinsolve). Often, it is not trivial do get something useful
    out of them.

    Parameters
    ==========

    n : int, optional
        In order to replace ImageSet with FiniteSet, an iterator is created
        for each ImageSet contained in `set_sol`, starting from 0 up to `n`.
        Default value: 10.
    """
    images = set_sol.find(ImageSet)
    for im in images:
        it = iter(im)
        s = FiniteSet(*[next(it) for n in range(0, n)])
        set_sol = set_sol.subs(im, s)
    return set_sol

