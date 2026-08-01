
def test_covar_deriv():
    ch = metric_to_Christoffel_2nd(TP(R2.dx, R2.dx) + TP(R2.dy, R2.dy))
    cvd = BaseCovarDerivativeOp(R2_r, 0, ch)
    assert cvd(R2.x) == 1
    # This line fails if the cache is disabled:
    assert cvd(R2.x*R2.e_x) == R2.e_x
    cvd = CovarDerivativeOp(R2.x*R2.e_x, ch)
    assert cvd(R2.x) == R2.x
    assert cvd(R2.x*R2.e_x) == R2.x*R2.e_x

