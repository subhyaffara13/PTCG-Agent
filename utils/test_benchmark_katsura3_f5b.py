
def test_benchmark_katsura3_f5b():
    with config.using(groebner='f5b'):
        _do_test_benchmark_katsura_3()

