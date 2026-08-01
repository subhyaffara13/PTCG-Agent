
def test_expn_large_n():
    # Test the transition to the asymptotic regime of n.
    dataset = []
    for n in [50, 51]:
        for x in np.logspace(0, 4, 200):
            with mpmath.workdps(100):
                dataset.append((n, x, float(mpmath.expint(n, x))))
    dataset = np.asarray(dataset)

    FuncData(sc.expn, dataset, (0, 1), 2, rtol=1e-13).check()

