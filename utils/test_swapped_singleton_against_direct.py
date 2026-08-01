
def test_swapped_singleton_against_direct(restore_singleton_bitgen):
    np.random.set_bit_generator(PCG64(98765))
    singleton_vals = np.random.randint(0, 2 ** 30, 10)
    rg = np.random.RandomState(PCG64(98765))
    non_singleton_vals = rg.randint(0, 2 ** 30, 10)
    assert_equal(non_singleton_vals, singleton_vals)

