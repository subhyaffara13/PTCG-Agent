
def test_lpmv():
    pts = []
    for x in [-0.99, -0.557, 1e-6, 0.132, 1]:
        pts.extend([
            (1, 1, x),
            (1, -1, x),
            (-1, 1, x),
            (-1, -2, x),
            (1, 1.7, x),
            (1, -1.7, x),
            (-1, 1.7, x),
            (-1, -2.7, x),
            (1, 10, x),
            (1, 11, x),
            (3, 8, x),
            (5, 11, x),
            (-3, 8, x),
            (-5, 11, x),
            (3, -8, x),
            (5, -11, x),
            (-3, -8, x),
            (-5, -11, x),
            (3, 8.3, x),
            (5, 11.3, x),
            (-3, 8.3, x),
            (-5, 11.3, x),
            (3, -8.3, x),
            (5, -11.3, x),
            (-3, -8.3, x),
            (-5, -11.3, x),
        ])

    def mplegenp(nu, mu, x):
        if mu == int(mu) and x == 1:
            # mpmath 0.17 gets this wrong
            if mu == 0:
                return 1
            else:
                return 0
        return mpmath.legenp(nu, mu, x)

    dataset = [p + (mplegenp(p[1], p[0], p[2]),) for p in pts]
    dataset = np.array(dataset, dtype=np.float64)

    def evf(mu, nu, x):
        return sc.lpmv(mu.astype(int), nu, x)

    with np.errstate(invalid='ignore'):
        FuncData(evf, dataset, (0,1,2), 3, rtol=1e-10, atol=1e-14).check()

