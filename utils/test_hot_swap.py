
def test_hot_swap(restore_singleton_bitgen):
    # GH 21808
    def_bg = np.random.default_rng(0)
    bg = def_bg.bit_generator
    np.random.set_bit_generator(bg)
    assert isinstance(np.random.mtrand._rand._bit_generator, type(bg))

    second_bg = np.random.get_bit_generator()
    assert bg is second_bg

