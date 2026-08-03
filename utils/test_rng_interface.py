import random

def test_rng_interface():
    global progress

    # try different kinds of seeds
    for seed in [14, np.random.RandomState(14)]:
        np.random.seed(42)
        random.seed(42)
        run_all_random_functions(seed)
        progress = 0

        # check that both global RNGs are unaffected
        after_np_rv = np.random.rand()
        #        if np_rv != after_np_rv:
        #            print(np_rv, after_np_rv, "don't match np!")
        assert np_rv == after_np_rv
        after_py_rv = random.random()
        #        if py_rv != after_py_rv:
        #            print(py_rv, after_py_rv, "don't match py!")
        assert py_rv == after_py_rv

