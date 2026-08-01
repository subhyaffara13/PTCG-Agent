
def test_swap_worked(restore_singleton_bitgen):
    # GH 21808
    np.random.seed(98765)
    vals = np.random.randint(0, 2 ** 30, 10)
    bg = PCG64(0)
    state = bg.state
    np.random.set_bit_generator(bg)
    state_direct = np.random.get_state(legacy=False)
    for field in state:
        assert state[field] == state_direct[field]
    np.random.seed(98765)
    pcg_vals = np.random.randint(0, 2 ** 30, 10)
    assert not np.all(vals == pcg_vals)
    new_state = bg.state
    assert new_state["state"]["state"] != state["state"]["state"]
    assert new_state["state"]["inc"] == new_state["state"]["inc"]

