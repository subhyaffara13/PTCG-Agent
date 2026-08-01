
def test_has_multiple():
    f = x**2*y + sin(2**t + log(z))

    assert f.has(x)
    assert f.has(y)
    assert f.has(z)
    assert f.has(t)

    assert not f.has(u)

    assert f.has(x, y, z, t)
    assert f.has(x, y, z, t, u)

    i = Integer(4400)

    assert not i.has(x)

    assert (i*x**i).has(x)
    assert not (i*y**i).has(x)
    assert (i*y**i).has(x, y)
    assert not (i*y**i).has(x, z)

