
def descendant_subgroups(S, C, R1_c_list, x, R2, N, Y):
    A_dict = C.A_dict
    A_dict_inv = C.A_dict_inv
    if C.is_complete():
        # if C is complete then it only needs to test
        # whether the relators in R2 are satisfied
        for w, alpha in product(R2, C.omega):
            if not C.scan_check(alpha, w):
                return
        # relators in R2 are satisfied, append the table to list
        S.append(C)
    else:
        # find the first undefined entry in Coset Table
        for alpha, x in product(range(len(C.table)), C.A):
            if C.table[alpha][A_dict[x]] is None:
                # this is "x" in pseudo-code (using "y" makes it clear)
                undefined_coset, undefined_gen = alpha, x
                break
        # for filling up the undefine entry we try all possible values
        # of beta in Omega or beta = n where beta^(undefined_gen^-1) is undefined
        reach = C.omega + [C.n]
        for beta in reach:
            if beta < N:
                if beta == C.n or C.table[beta][A_dict_inv[undefined_gen]] is None:
                    try_descendant(S, C, R1_c_list, R2, N, undefined_coset, \
                            undefined_gen, beta, Y)

