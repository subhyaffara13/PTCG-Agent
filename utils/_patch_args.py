
def _patch_args(func_name, args):
    '''Make sure func(*args) does not raise because *args is wrong.'''
    if func_name == 'cdf2rdf':
        args = (args[0][0], args[1])  # cdf2rd(1d, 2d)
    elif func_name == 'funm':
        args = (args[0], lambda x: x)
    elif func_name == 'lu_solve':
        a = args[0]
        piv = np.arange(a.shape[0])
        args = ((a, piv), args[1])
    elif func_name in ('eigh_tridiagonal', 'eigvalsh_tridiagonal'):       
        d, e = args
        args = (d, e[:, :-1])
    elif func_name == 'cossin':
        a = args[0]
        args = (a, a.shape[0]//2, a.shape[1]//2)
    elif func_name == 'solve_banded':
        from scipy.linalg._basic import _to_banded
        args = ((1, 2), _to_banded(1, 2, args[0]), args[0])
    elif func_name == 'solveh_banded':
        from scipy.linalg._basic import _to_banded
        args = (_to_banded(0, 2, args[0])[:, :-1], args[0][0, :-1])
    elif func_name == 'cholesky_banded':
        from scipy.linalg._basic import _to_banded
        args = (_to_banded(0, 2, args[0])[:, :-1],)
    elif func_name == 'solve_toeplitz':
        c = args[0][1]
        args = (c, np.ones_like(c))
    return args

