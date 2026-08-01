
def test_Poisson():
    l = 3
    x = Poisson('x', l)
    assert E(x) == l
    assert E(2*x) == 2*l
    assert variance(x) == l
    assert density(x) == PoissonDistribution(l)
    assert isinstance(E(x, evaluate=False), Expectation)
    assert isinstance(E(2*x, evaluate=False), Expectation)
    # issue 8248
    assert x.pspace.compute_expectation(1) == 1
    # issue 27344
    try:
        import numpy as np
    except ImportError:
        skip("numpy not installed")
    y = Poisson('y', np.float64(4.72544290380919e-11))
    assert E(y) == 4.72544290380919e-11
    y = Poisson('y', np.float64(4.725442903809197e-11))
    assert E(y) == 4.725442903809197e-11
    l2 = 5
    z = Poisson('z', l2)
    assert E(z) == l2
    assert E(FallingFactorial(z, 3)) == l2**3
    assert E(z**2) == l2 + l2**2

