
def test_operator_match():
    """Test that the output of dot, cross, outer functions match
    operator behavior.
    """
    A = ReferenceFrame('A')
    v = A.x + A.y
    d = v | v
    zerov = Vector(0)
    zerod = Dyadic(0)

    # dot products
    assert d & d == dot(d, d)
    assert d & zerod == dot(d, zerod)
    assert zerod & d == dot(zerod, d)
    assert d & v == dot(d, v)
    assert v & d == dot(v, d)
    assert d & zerov == dot(d, zerov)
    assert zerov & d == dot(zerov, d)
    raises(TypeError, lambda: dot(d, S.Zero))
    raises(TypeError, lambda: dot(S.Zero, d))
    raises(TypeError, lambda: dot(d, 0))
    raises(TypeError, lambda: dot(0, d))
    assert v & v == dot(v, v)
    assert v & zerov == dot(v, zerov)
    assert zerov & v == dot(zerov, v)
    raises(TypeError, lambda: dot(v, S.Zero))
    raises(TypeError, lambda: dot(S.Zero, v))
    raises(TypeError, lambda: dot(v, 0))
    raises(TypeError, lambda: dot(0, v))

    # cross products
    raises(TypeError, lambda: cross(d, d))
    raises(TypeError, lambda: cross(d, zerod))
    raises(TypeError, lambda: cross(zerod, d))
    assert d ^ v == cross(d, v)
    assert v ^ d == cross(v, d)
    assert d ^ zerov == cross(d, zerov)
    assert zerov ^ d == cross(zerov, d)
    assert zerov ^ d == cross(zerov, d)
    raises(TypeError, lambda: cross(d, S.Zero))
    raises(TypeError, lambda: cross(S.Zero, d))
    raises(TypeError, lambda: cross(d, 0))
    raises(TypeError, lambda: cross(0, d))
    assert v ^ v == cross(v, v)
    assert v ^ zerov == cross(v, zerov)
    assert zerov ^ v == cross(zerov, v)
    raises(TypeError, lambda: cross(v, S.Zero))
    raises(TypeError, lambda: cross(S.Zero, v))
    raises(TypeError, lambda: cross(v, 0))
    raises(TypeError, lambda: cross(0, v))

    # outer products
    raises(TypeError, lambda: outer(d, d))
    raises(TypeError, lambda: outer(d, zerod))
    raises(TypeError, lambda: outer(zerod, d))
    raises(TypeError, lambda: outer(d, v))
    raises(TypeError, lambda: outer(v, d))
    raises(TypeError, lambda: outer(d, zerov))
    raises(TypeError, lambda: outer(zerov, d))
    raises(TypeError, lambda: outer(zerov, d))
    raises(TypeError, lambda: outer(d, S.Zero))
    raises(TypeError, lambda: outer(S.Zero, d))
    raises(TypeError, lambda: outer(d, 0))
    raises(TypeError, lambda: outer(0, d))
    assert v | v == outer(v, v)
    assert v | zerov == outer(v, zerov)
    assert zerov | v == outer(zerov, v)
    raises(TypeError, lambda: outer(v, S.Zero))
    raises(TypeError, lambda: outer(S.Zero, v))
    raises(TypeError, lambda: outer(v, 0))
    raises(TypeError, lambda: outer(0, v))

