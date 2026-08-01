
def test_multivar_3():
    assert (Order(x) + Order(y)).args in [
        (Order(x), Order(y)),
        (Order(y), Order(x))]
    assert Order(x) + Order(y) + Order(x + y) == Order(x + y)
    assert (Order(x**2*y) + Order(y**2*x)).args in [
        (Order(x*y**2), Order(y*x**2)),
        (Order(y*x**2), Order(x*y**2))]
    assert (Order(x**2*y) + Order(y*x)) == Order(x*y)

