
def test_runtime_warning():
    with pytest.warns(RuntimeWarning,
                      match=r'Too many predicted coefficients'):
        mathieu_odd_coef(1000, 1000)
    with pytest.warns(RuntimeWarning,
                      match=r'Too many predicted coefficients'):
        mathieu_even_coef(1000, 1000)

