
def test_uniform_P():
    """ This stopped working because SingleContinuousPSpace.compute_density no
    longer calls integrate on a DiracDelta but rather just solves directly.
    integrate used to call UniformDistribution.expectation which special-cased
    subsed out the Min and Max terms that Uniform produces

    I decided to regress on this class for general cleanliness (and I suspect
    speed) of the algorithm.
    """
    l = Symbol('l', real=True)
    w = Symbol('w', positive=True)
    X = Uniform('x', l, l + w)
    assert P(X < l) == 0 and P(X > l + w) == 0

