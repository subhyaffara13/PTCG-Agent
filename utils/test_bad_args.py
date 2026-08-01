
def test_bad_args():
    # no vargs given
    raises(TypeError, lambda: lambdify(1))
    # same with vector exprs
    raises(TypeError, lambda: lambdify([1, 2]))


def test_bad_args():
    # loc and scale must be scalar
    with pytest.raises(ValueError, match="loc must be scalar"):
        FastGeneratorInversion(stats.norm(loc=(1.2, 1.3)))
    with pytest.raises(ValueError, match="scale must be scalar"):
        FastGeneratorInversion(stats.norm(scale=[1.5, 5.7]))

    with pytest.raises(ValueError, match="'test' cannot be used to seed"):
        FastGeneratorInversion(stats.norm(), random_state="test")

    msg = "Each of the 1 shape parameters must be a scalar"
    with pytest.raises(ValueError, match=msg):
        FastGeneratorInversion(stats.gamma([1.3, 2.5]))

    with pytest.raises(ValueError, match="`dist` must be a frozen"):
        FastGeneratorInversion("xy")

    with pytest.raises(ValueError, match="Distribution 'truncnorm' is not"):
        FastGeneratorInversion(stats.truncnorm(1.3, 4.5))

