
def test_single_arg_integer_exception(high, endpoint):
    # GH 14333
    gen = Generator(MT19937(0))
    msg = 'high < 0' if endpoint else 'high <= 0'
    with pytest.raises(ValueError, match=msg):
        gen.integers(high, endpoint=endpoint)
    msg = 'low > high' if endpoint else 'low >= high'
    with pytest.raises(ValueError, match=msg):
        gen.integers(-1, high, endpoint=endpoint)
    with pytest.raises(ValueError, match=msg):
        gen.integers([-1], high, endpoint=endpoint)

