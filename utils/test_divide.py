import math


def test_divide(a_shape, b_shape):
    rng = np.random.default_rng(23409823)
    a = random_array(a_shape, density=0.6, random_state=rng, dtype=int)
    b = np.arange(1, 1 + math.prod(b_shape)).reshape(b_shape)
    res = a / b
    exp = a.toarray() / b
    assert_allclose(res.toarray(), exp)

    res = a / b
    assert_allclose(res.toarray(), exp)

