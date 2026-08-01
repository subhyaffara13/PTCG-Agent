
def test_malformed1():
    # Example from gh-6072
    # Contains malformed header data, which previously resulted into a
    # buffer overflow.
    #
    # Should raise an exception, not segfault
    fname = pjoin(TEST_DATA_PATH, 'malformed1.mat')
    with open(fname, 'rb') as f:
        assert_raises(ValueError, loadmat, f)

