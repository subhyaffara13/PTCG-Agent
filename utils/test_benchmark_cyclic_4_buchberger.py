
def test_benchmark_cyclic_4_buchberger():
    with config.using(groebner='buchberger'):
        _do_test_benchmark_cyclic_4()

