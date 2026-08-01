
def test_issue_5933():
    from sympy.geometry.polygon import (Polygon, RegularPolygon)
    from sympy.simplify.radsimp import denom
    x = Polygon(*RegularPolygon((0, 0), 1, 5).vertices).centroid.x
    assert abs(denom(x).n()) > 1e-12
    assert abs(denom(radsimp(x))) > 1e-12  # in case simplify didn't handle it

