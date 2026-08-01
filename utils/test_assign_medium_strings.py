
def test_assign_medium_strings():
    # see gh-29261
    N = 9
    src = np.array(
        (
            ['0' * 256] * 3 + ['0' * 255] + ['0' * 256] + ['0' * 255] +
            ['0' * 256] * 2 + ['0' * 255]
        ), dtype='T')
    dst = np.array(
        (
            ['0' * 255] + ['0' * 256] * 2 + ['0' * 255] + ['0' * 256] +
            ['0' * 255] + [''] * 5
        ), dtype='T')

    dst[1:N + 1] = src
    assert_array_equal(dst[1:N + 1], src)

