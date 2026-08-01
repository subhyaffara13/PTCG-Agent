
def test_state_error_alt_bit_gen(restore_singleton_bitgen):
    # GH 21808
    state = np.random.get_state()
    bg = PCG64(0)
    np.random.set_bit_generator(bg)
    with pytest.raises(ValueError, match="state must be for a PCG64"):
        np.random.set_state(state)

