
def test_seed_alt_bit_gen(restore_singleton_bitgen):
    # GH 21808
    bg = PCG64(0)
    np.random.set_bit_generator(bg)
    state = np.random.get_state(legacy=False)
    np.random.seed(1)
    new_state = np.random.get_state(legacy=False)
    print(state)
    print(new_state)
    assert state["bit_generator"] == "PCG64"
    assert state["state"]["state"] != new_state["state"]["state"]
    assert state["state"]["inc"] != new_state["state"]["inc"]

