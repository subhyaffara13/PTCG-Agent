
def test_gh9551_raise_error_if_disp_true():
    """Test that if disp is true then zero derivative raises RuntimeError"""

    def f(x):
        return x*x + 1

    def f_p(x):
        return 2*x

    with pytest.warns(RuntimeWarning):
        zeros.newton(f, 1.0, f_p, disp=False)
    with pytest.raises(
            RuntimeError,
            match=r'^Derivative was zero\. Failed to converge after \d+ iterations, '
                  r'value is [+-]?\d*\.\d+\.$'):
        zeros.newton(f, 1.0, f_p)
    root = zeros.newton(f, complex(10.0, 10.0), f_p)
    assert_allclose(root, complex(0.0, 1.0))

