
def check_2drbf1d_regularity(function, atol):
    # Check that the 2-D Rbf function approximates a smooth function well away
    # from the nodes.
    x = linspace(0, 10, 9)
    y0 = sin(x)
    y1 = cos(x)
    y = np.vstack([y0, y1]).T
    rbf = Rbf(x, y, function=function, mode='N-D')
    xi = linspace(0, 10, 100)
    yi = rbf(xi)
    msg = f"abs-diff: {abs(yi - np.vstack([sin(xi), cos(xi)]).T).max():f}"
    assert allclose(yi, np.vstack([sin(xi), cos(xi)]).T, atol=atol), msg

