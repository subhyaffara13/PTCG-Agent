
def test_benchmark_minpoly_buchberger():
    with config.using(groebner='buchberger'):
        _do_test_benchmark_minpoly()

