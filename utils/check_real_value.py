
def check_real_value(f, x1, y1, x, exact=True):
    z1 = np.array([complex(x1, y1)])
    if exact:
        assert_equal(f(z1), x)
    else:
        assert_almost_equal(f(z1), x)

