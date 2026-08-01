
def define_schreier_generators(C, homomorphism=False):
    '''
    Parameters
    ==========

    C -- Coset table.
    homomorphism -- When set to True, return a dictionary containing the images
                     of the presentation generators in the original group.
    '''
    y = []
    gamma = 1
    f = C.fp_group
    X = f.generators
    if homomorphism:
        # `_gens` stores the elements of the parent group to
        # to which the schreier generators correspond to.
        _gens = {}
        # compute the schreier Traversal
        tau = {}
        tau[0] = f.identity
    C.P = [[None]*len(C.A) for i in range(C.n)]
    for alpha, x in product(C.omega, C.A):
        beta = C.table[alpha][C.A_dict[x]]
        if beta == gamma:
            C.P[alpha][C.A_dict[x]] = "<identity>"
            C.P[beta][C.A_dict_inv[x]] = "<identity>"
            gamma += 1
            if homomorphism:
                tau[beta] = tau[alpha]*x
        elif x in X and C.P[alpha][C.A_dict[x]] is None:
            y_alpha_x = '%s_%s' % (x, alpha)
            y.append(y_alpha_x)
            C.P[alpha][C.A_dict[x]] = y_alpha_x
            if homomorphism:
                _gens[y_alpha_x] = tau[alpha]*x*tau[beta]**-1
    grp_gens = list(free_group(', '.join(y)))
    C._schreier_free_group = grp_gens.pop(0)
    C._schreier_generators = grp_gens
    if homomorphism:
        C._schreier_gen_elem = _gens
    # replace all elements of P by, free group elements
    for i, j in product(range(len(C.P)), range(len(C.A))):
        # if equals "<identity>", replace by identity element
        if C.P[i][j] == "<identity>":
            C.P[i][j] = C._schreier_free_group.identity
        elif isinstance(C.P[i][j], str):
            r = C._schreier_generators[y.index(C.P[i][j])]
            C.P[i][j] = r
            beta = C.table[i][j]
            C.P[beta][j + 1] = r**-1

