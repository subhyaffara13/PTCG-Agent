
def test_gammainc_boundary():
    # Test the transition to the asymptotic series.
    small = 20
    a = np.linspace(0.5*small, 2*small, 50)
    x = a.copy()
    a, x = np.meshgrid(a, x)
    a, x = a.flatten(), x.flatten()
    with mpmath.workdps(100):
        dataset = [(a0, x0, float(mpmath.gammainc(a0, b=x0, regularized=True)))
                   for a0, x0 in zip(a, x)]
    dataset = np.array(dataset)

    FuncData(sc.gammainc, dataset, (0, 1), 2, rtol=1e-12).check()

