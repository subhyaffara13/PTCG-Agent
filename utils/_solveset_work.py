
def _solveset_work(system, symbols):
    soln = solveset(system[0], symbols[0])
    if isinstance(soln, FiniteSet):
        _soln = FiniteSet(*[(s,) for s in soln])
        return _soln
    else:
        return FiniteSet(tuple(FiniteSet(soln)))

