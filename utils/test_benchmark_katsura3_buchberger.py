
def test_benchmark_katsura3_buchberger():
    with config.using(groebner='buchberger'):
        _do_test_benchmark_katsura_3()

