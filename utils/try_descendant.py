
def try_descendant(S, C, R1_c_list, R2, N, alpha, x, beta, Y):
    r"""
    Solves the problem of trying out each individual possibility
    for `\alpha^x.

    """
    D = C.copy()
    if beta == D.n and beta < N:
        D.table.append([None]*len(D.A))
        D.p.append(beta)
    D.table[alpha][D.A_dict[x]] = beta
    D.table[beta][D.A_dict_inv[x]] = alpha
    D.deduction_stack.append((alpha, x))
    if not D.process_deductions_check(R1_c_list[D.A_dict[x]], \
            R1_c_list[D.A_dict_inv[x]]):
        return
    for w in Y:
        if not D.scan_check(0, w):
            return
    if first_in_class(D, Y):
        descendant_subgroups(S, D, R1_c_list, x, R2, N, Y)

