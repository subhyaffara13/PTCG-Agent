
def test_benchmark_kastura_4_buchberger():
    with config.using(groebner='buchberger'):
        _do_test_benchmark_katsura_4()

