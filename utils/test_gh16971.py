
def test_gh16971():
    def cons(x):
        return np.sum(x**2) - 0

    c = {'fun': cons, 'type': 'ineq'}
    minimizer_kwargs = {
        'method': 'COBYLA',
        'options': {'rhobeg': 5, 'tol': 5e-1, 'catol': 0.05}
    }

    s = SHGO(
        rosen, [(0, 10)]*2, constraints=c, minimizer_kwargs=minimizer_kwargs
    )

    assert s.minimizer_kwargs['method'].lower() == 'cobyla'
    assert s.minimizer_kwargs['options']['catol'] == 0.05

