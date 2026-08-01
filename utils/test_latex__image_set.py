
def test_latex_ImageSet():
    x = Symbol('x')
    assert latex(ImageSet(Lambda(x, x**2), S.Naturals)) == \
        r"\left\{x^{2}\; \middle|\; x \in \mathbb{N}\right\}"

    y = Symbol('y')
    imgset = ImageSet(Lambda((x, y), x + y), {1, 2, 3}, {3, 4})
    assert latex(imgset) == \
        r"\left\{x + y\; \middle|\; x \in \left\{1, 2, 3\right\}, y \in \left\{3, 4\right\}\right\}"

    imgset = ImageSet(Lambda(((x, y),), x + y), ProductSet({1, 2, 3}, {3, 4}))
    assert latex(imgset) == \
        r"\left\{x + y\; \middle|\; \left( x, \  y\right) \in \left\{1, 2, 3\right\} \times \left\{3, 4\right\}\right\}"

