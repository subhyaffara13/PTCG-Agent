
def test_identical_conds_issue():
    from sympy.stats import Uniform, density
    u1 = Uniform('u1', 0, 1)
    u2 = Uniform('u2', 0, 1)
    # Result is quite big, so not really important here (and should ideally be
    # simpler). Should not give an exception though.
    density(u1 + u2)

