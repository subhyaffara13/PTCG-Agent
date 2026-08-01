
def test_digamma_roots():
    # Test the special-cased roots for digamma.
    root = mpmath.findroot(mpmath.digamma, 1.5)
    roots = [float(root)]
    root = mpmath.findroot(mpmath.digamma, -0.5)
    roots.append(float(root))
    roots = np.array(roots)

    # If we test beyond a radius of 0.24 mpmath will take forever.
    dx = np.r_[-0.24, -np.logspace(-1, -15, 10), 0, np.logspace(-15, -1, 10), 0.24]
    dy = dx.copy()
    dx, dy = np.meshgrid(dx, dy)
    dz = dx + 1j*dy
    z = (roots + np.dstack((dz,)*roots.size)).flatten()
    with mpmath.workdps(30):
        dataset = [(z0, complex(mpmath.digamma(z0))) for z0 in z]

    dataset = np.array(dataset)
    FuncData(sc.digamma, dataset, 0, 1, rtol=1e-14).check()

