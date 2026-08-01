
def test_benchmark_minpoly_f5b():
    with config.using(groebner='f5b'):
        _do_test_benchmark_minpoly()

