
def test_groebner_buchberger():
    with config.using(groebner='buchberger'):
        _do_test_groebner()

