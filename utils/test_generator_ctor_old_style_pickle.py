
def test_generator_ctor_old_style_pickle():
    rg = np.random.Generator(np.random.PCG64DXSM(0))
    rg.standard_normal(1)
    # Directly call reduce which is used in pickling
    ctor, (bit_gen, ), _ = rg.__reduce__()
    # Simulate unpickling an old pickle that only has the name
    assert bit_gen.__class__.__name__ == "PCG64DXSM"
    print(ctor)
    b = ctor(*("PCG64DXSM",))
    print(b)
    b.bit_generator.state = bit_gen.state
    state_b = b.bit_generator.state
    assert bit_gen.state == state_b

