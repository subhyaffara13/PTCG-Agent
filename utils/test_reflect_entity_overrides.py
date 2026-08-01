
def test_reflect_entity_overrides():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    b = Symbol('b')
    m = Symbol('m')
    l = Line((0, b), slope=m)
    p = Point(x, y)
    r = p.reflect(l)
    c = Circle((x, y), 3)
    cr = c.reflect(l)
    assert cr == Circle(r, -3)
    assert c.area == -cr.area

    pent = RegularPolygon((1, 2), 1, 5)
    slope = S.ComplexInfinity
    while slope is S.ComplexInfinity:
        slope = Rational(*(x._random()/2).as_real_imag())
    l = Line(pent.vertices[1], slope=slope)
    rpent = pent.reflect(l)
    assert rpent.center == pent.center.reflect(l)
    rvert = [i.reflect(l) for i in pent.vertices]
    for v in rpent.vertices:
        for i in range(len(rvert)):
            ri = rvert[i]
            if ri.equals(v):
                rvert.remove(ri)
                break
    assert not rvert
    assert pent.area.equals(-rpent.area)

