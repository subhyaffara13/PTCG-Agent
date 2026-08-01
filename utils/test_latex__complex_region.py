
def test_latex_ComplexRegion():
    assert latex(ComplexRegion(Interval(3, 5)*Interval(4, 6))) == \
        r"\left\{x + y i\; \middle|\; x, y \in \left[3, 5\right] \times \left[4, 6\right] \right\}"
    assert latex(ComplexRegion(Interval(0, 1)*Interval(0, 2*pi), polar=True)) == \
        r"\left\{r \left(i \sin{\left(\theta \right)} + \cos{\left(\theta "\
        r"\right)}\right)\; \middle|\; r, \theta \in \left[0, 1\right] \times \left[0, 2 \pi\right) \right\}"

