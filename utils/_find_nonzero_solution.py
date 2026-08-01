
def _find_nonzero_solution(r, homosys):
    ones = lambda shape: DomainMatrix.ones(shape, r.domain)
    particular, nullspace = r._solve(homosys)
    nullity = nullspace.shape[0]
    nullpart = ones((1, nullity)) * nullspace
    sol = (particular + nullpart).transpose()
    return sol

