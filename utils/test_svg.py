
def test_svg():
    e1 = Ellipse(Point(1, 0), 3, 2)
    assert e1._svg(2, "#FFAAFF") == '<ellipse fill="#FFAAFF" stroke="#555555" stroke-width="4.0" opacity="0.6" cx="1.00000000000000" cy="0" rx="3.00000000000000" ry="2.00000000000000"/>'


def test_svg():
    a = Symbol('a')
    b = Symbol('b')
    d = Symbol('d')

    entity = Circle(Point(a, b), d)
    assert entity._repr_svg_() is None

    entity = Circle(Point(0, 0), S.Infinity)
    assert entity._repr_svg_() is None


def test_svg():
    a = Line(Point(1, 1),Point(1, 2))
    assert a._svg() == '<path fill-rule="evenodd" fill="#66cc99" stroke="#555555" stroke-width="2.0" opacity="0.6" d="M 1.00000000000000,1.00000000000000 L 1.00000000000000,2.00000000000000" marker-start="url(#markerReverseArrow)" marker-end="url(#markerArrow)"/>'
    a = Segment(Point(1, 0),Point(1, 1))
    assert a._svg() == '<path fill-rule="evenodd" fill="#66cc99" stroke="#555555" stroke-width="2.0" opacity="0.6" d="M 1.00000000000000,0 L 1.00000000000000,1.00000000000000" />'
    a = Ray(Point(2, 3), Point(3, 5))
    assert a._svg() == '<path fill-rule="evenodd" fill="#66cc99" stroke="#555555" stroke-width="2.0" opacity="0.6" d="M 2.00000000000000,3.00000000000000 L 3.00000000000000,5.00000000000000" marker-start="url(#markerCircle)" marker-end="url(#markerArrow)"/>'

