
def test_subclassing_QMCEngine():
    engine = RandomEngine(2, rng=175180605424926556207367152557812293274)

    sample_1 = engine.random(n=5)
    sample_2 = engine.random(n=7)
    assert engine.num_generated == 12

    # reset and re-sample
    engine.reset()
    assert engine.num_generated == 0

    sample_1_test = engine.random(n=5)
    assert_equal(sample_1, sample_1_test)

    # repeat reset and fast forward
    engine.reset()
    engine.fast_forward(n=5)
    sample_2_test = engine.random(n=7)

    assert_equal(sample_2, sample_2_test)
    assert engine.num_generated == 12

