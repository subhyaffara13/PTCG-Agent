
def _l_p_exact(L, m, n):
    '''Calculate the p-value of Page's L exactly'''
    # [1] uses m, n; [5] uses n, k.
    # Switch convention here because exact calculation code references [5].
    L, n, k = int(L), int(m), int(n)
    _pagel_state.state.set_k(k)
    return _pagel_state.state.sf(L, n)

