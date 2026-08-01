
def test_latex_ConditionSet():
    x = Symbol('x')
    assert latex(ConditionSet(x, Eq(x**2, 1), S.Reals)) == \
        r"\left\{x\; \middle|\; x \in \mathbb{R} \wedge x^{2} = 1 \right\}"
    assert latex(ConditionSet(x, Eq(x**2, 1), S.UniversalSet)) == \
        r"\left\{x\; \middle|\; x^{2} = 1 \right\}"

