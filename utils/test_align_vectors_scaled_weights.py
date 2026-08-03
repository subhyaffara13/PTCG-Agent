import math


def test_align_vectors_scaled_weights(xp):
    n = 10
    a = xp.asarray(Rotation.random(n, rng=0).apply([1, 0, 0]))
    b = xp.asarray(Rotation.random(n, rng=1).apply([1, 0, 0]))
    scale = 2

    est1, rssd1, cov1 = Rotation.align_vectors(a, b, xp.ones(n), True)
    est2, rssd2, cov2 = Rotation.align_vectors(a, b, scale * xp.ones(n), True)

    xp_assert_close(est1.as_matrix(), est2.as_matrix())
    xp_assert_close(math.sqrt(scale) * rssd1, rssd2, atol=1e-6)
    xp_assert_close(cov1, cov2)

