
def assert_mt19937_state_equal(a, b):
    assert_equal(a['bit_generator'], b['bit_generator'])
    assert_array_equal(a['state']['key'], b['state']['key'])
    assert_array_equal(a['state']['pos'], b['state']['pos'])
    assert_equal(a['has_gauss'], b['has_gauss'])
    assert_equal(a['gauss'], b['gauss'])

