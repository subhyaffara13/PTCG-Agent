
def test_whittaker_small_data():
    """Test that whittaker works on a few data points."""
    # Should work on order + 1 data points. The first 2*order+1 are special.
    la = 1
    y = np.arange(2)
    wh = whittaker_henderson(y, order=1, lamb=la)
    # Analytical solution for order=1 and n=2
    res = (np.array([[1 + la, la], [la, 1 + la]]) / (1 + 2 * la)) @ y
    assert_allclose(wh.x, res, atol=1e-15)
    whittaker_henderson(np.arange(3), order=1, lamb=la)

    y = np.arange(3)
    wh = whittaker_henderson(y, order=2, lamb=la)
    # Analytical solution for order=2 and n=3:
    # import numpy as np
    # from sympy import eye, Symbol
    # n, order = 3, 2
    # la = Symbol("la")
    # D = np.diff(eye(n), n=order, axis=0)
    # A = eye(n) + la * D.T @ D
    # A.inv()
    res = (
        np.array([
            [1 + 5 * la,     2 * la,        -la],
            [    2 * la, 1 + 2 * la,     2 * la],
            [       -la,     2 * la, 1 + 5 * la],
        ]) / (1 + 6 * la)) @ y
    assert_allclose(wh.x, res, atol=1e-15)
    assert wh.lamb == la
    
    y = np.arange(4)
    wh = whittaker_henderson(y, order=2, lamb=la)
    la2 = la ** 2
    res =(np.array([
        [14*la2 + 11*la + 1, 8*la2 + 2*la    , 2*la2 -   la,     -4*la2            ],
        [ 8*la2 +  2*la    , 6*la2 + 7*la + 1, 4*la2 + 4*la,      2*la2 -  la      ],
        [ 2*la2 -    la    , 4*la2 + 4*la    , 6*la2 + 7*la + 1,  8*la2 + 2*la     ],
        [-4*la2            , 2*la2 -   la    , 8*la2 + 2*la    , 14*la2 + 11*la + 1],
    ]) /(20*la2 + 12*la + 1)) @ y
    assert_allclose(wh.x, res, atol=1e-15)
    whittaker_henderson(np.arange(5), order=2, lamb=la)

    whittaker_henderson(np.arange(4), order=3, lamb=la)
    whittaker_henderson(np.arange(5), order=3, lamb=la)
    whittaker_henderson(np.arange(6), order=3, lamb=la)
    whittaker_henderson(np.arange(7), order=3, lamb=la)

