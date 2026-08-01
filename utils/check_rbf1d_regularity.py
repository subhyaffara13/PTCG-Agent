
def check_rbf1d_regularity(function, atol):
    # Check that the Rbf function approximates a smooth function well away
    # from the nodes.
    x = linspace(0, 10, 9)
    y = sin(x)
    rbf = Rbf(x, y, function=function)
    xi = linspace(0, 10, 100)
    yi = rbf(xi)
    msg = f"abs-diff: {abs(yi - sin(xi)).max():f}"
    assert allclose(yi, sin(xi), atol=atol), msg

