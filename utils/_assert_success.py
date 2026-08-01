
def _assert_success(*, A, x, b, xp, rtol=1.0, atol=0.0, less_equal=False):
    Ax = xp.squeeze(A @ x[..., xp.newaxis], axis=-1)
    residual = Ax - b
    err = xp_vector_norm(residual, axis=-1)
    assertion = xp_assert_less_equal if less_equal else xp_assert_less
    limit = atol + rtol * xp_vector_norm(b, axis=-1)
    assertion(err, limit)


def _assert_success(res, desired_fun=None, desired_x=None,
                    rtol=1e-8, atol=1e-8):
    # res: linprog result object
    # desired_fun: desired objective function value or None
    # desired_x: desired solution or None
    if not res.success:
        msg = f"linprog status {res.status}, message: {res.message}"
        raise AssertionError(msg)

    assert_equal(res.status, 0)
    if desired_fun is not None:
        assert_allclose(res.fun, desired_fun,
                        err_msg="converged to an unexpected objective value",
                        rtol=rtol, atol=atol)
    if desired_x is not None:
        assert_allclose(res.x, desired_x,
                        err_msg="converged to an unexpected solution",
                        rtol=rtol, atol=atol)

