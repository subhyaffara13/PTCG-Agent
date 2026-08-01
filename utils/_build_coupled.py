
def _build_coupled(jcoupling, length):
    n_list = [ [n + 1] for n in range(length) ]
    coupled_jn = []
    coupled_n = []
    for n1, n2, j_new in jcoupling:
        coupled_jn.append(j_new)
        coupled_n.append( (n_list[n1 - 1], n_list[n2 - 1]) )
        n_sort = sorted(n_list[n1 - 1] + n_list[n2 - 1])
        n_list[n_sort[0] - 1] = n_sort
    return coupled_n, coupled_jn

