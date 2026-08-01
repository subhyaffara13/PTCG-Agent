
def test_ragged_shuffle():
    # GH 18142
    seq = [[], [], 1]
    gen = Generator(MT19937(0))
    assert_no_warnings(gen.shuffle, seq)
    assert seq == [1, [], []]

