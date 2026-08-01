
def test_latex_intersection():
    assert latex(Intersection(Interval(0, 1), Interval(x, y))) == \
        r"\left[0, 1\right] \cap \left[x, y\right]"

