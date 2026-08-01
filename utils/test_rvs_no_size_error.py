
def test_rvs_no_size_error():
    # _rvs methods must have parameter `size`; see gh-11394
    class rvs_no_size_gen(stats.rv_continuous):
        def _rvs(self):
            return 1

    rvs_no_size = rvs_no_size_gen(name='rvs_no_size')
    rng = np.random.default_rng(1334886239)
    with assert_raises(TypeError, match=r"_rvs\(\) got (an|\d) unexpected"):
        rvs_no_size.rvs(random_state=rng)

