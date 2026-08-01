
def test_gh_25180():
    lu = _LogUniform(log_a=np.float64(-0.28915434544814245),
                     log_b=np.float64(0.3085224670197856))
    actual = lu.mode(method='optimization')
    assert np.isfinite(actual)

