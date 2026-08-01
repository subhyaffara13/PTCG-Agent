
def test_pickle_preserves_seed_sequence():
    # GH 26234
    # Add explicit test that bit generators preserve seed sequences
    import pickle

    rg = np.random.Generator(np.random.PCG64DXSM(20240411))
    ss = rg.bit_generator.seed_seq
    rg_plk = pickle.loads(pickle.dumps(rg))
    ss_plk = rg_plk.bit_generator.seed_seq
    assert_equal(ss.state, ss_plk.state)
    assert_equal(ss.pool, ss_plk.pool)

    rg.bit_generator.seed_seq.spawn(10)
    rg_plk = pickle.loads(pickle.dumps(rg))
    ss_plk = rg_plk.bit_generator.seed_seq
    assert_equal(ss.state, ss_plk.state)

