
def test_output_len_long_input(xp):
    # Regression test for gh-17375.  On Windows, a large enough input
    # that should have been well within the capabilities of 64 bit integers
    # would result in a 32 bit overflow because of a bug in Cython 0.29.32.
    len_h = 1001
    in_len = 10**8
    up = 320
    down = 441
    out_len = _output_len(len_h, in_len, up, down)
    # The expected value was computed "by hand" from the formula
    #   (((in_len - 1) * up + len_h) - 1) // down + 1
    assert out_len == 72562360

