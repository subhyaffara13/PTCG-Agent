
def test_PolyElement_subresultants():
    R, x, y = ring("x, y", ZZ)

    f, g = x**2*y + x*y, x + y # degree(f, x) > degree(g, x)
    h = y**3 - y**2
    assert f.subresultants(g) == [f, g, h] # first generator is chosen default

    # generator index or generator is given
    assert f.subresultants(g, 0) ==  f.subresultants(g, x) == [f, g, h]

    assert f.subresultants(g, y) == [x**2*y + x*y, x + y, x**3 + x**2]

    f, g = 2*x - y, x**2 + 2*y + x # degree(f, x) < degree(g, x)
    assert f.subresultants(g) == [x**2 + x + 2*y, 2*x - y, y**2 + 10*y]

    f, g = R(0), y**3 - y**2 # f = 0
    assert f.subresultants(g) == [y**3 - y**2, 1]

    f, g = x**2*y + x*y, R(0) # g = 0
    assert f.subresultants(g) == [x**2*y + x*y, 1]

    f, g = R(0), R(0) # f = 0 and g = 0
    assert f.subresultants(g) == [0, 0]

    f, g = x**2 + x, x**2 + x # f and g are same polynomial
    assert f.subresultants(g) == [x**2 + x, x**2 + x]

