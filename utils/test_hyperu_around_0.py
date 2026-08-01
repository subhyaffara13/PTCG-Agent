
def test_hyperu_around_0():
    dataset = []
    # DLMF 13.2.14-15 test points.
    for n in np.arange(-5, 5):
        for b in np.linspace(-5, 5, 20):
            a = -n
            dataset.append((a, b, 0, float(mpmath.hyperu(a, b, 0))))
            a = -n + b - 1
            dataset.append((a, b, 0, float(mpmath.hyperu(a, b, 0))))
    # DLMF 13.2.16-22 test points.
    for a in [-10.5, -1.5, -0.5, 0, 0.5, 1, 10]:
        for b in [-1.0, -0.5, 0, 0.5, 1, 1.5, 2, 2.5]:
            dataset.append((a, b, 0, float(mpmath.hyperu(a, b, 0))))
    dataset = np.array(dataset)

    FuncData(sc.hyperu, dataset, (0, 1, 2), 3, rtol=1e-15, atol=5e-13).check()

