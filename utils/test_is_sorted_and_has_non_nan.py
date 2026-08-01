
def test_is_sorted_and_has_non_nan():
    assert _path.is_sorted_and_has_non_nan(np.array([1, 2, 3]))
    assert _path.is_sorted_and_has_non_nan(np.array([1, np.nan, 3]))
    assert not _path.is_sorted_and_has_non_nan([3, 5] + [np.nan] * 100 + [0, 2])
    # [2, 256] byteswapped:
    assert not _path.is_sorted_and_has_non_nan(np.array([33554432, 65536], ">i4"))
    n = 2 * mlines.Line2D._subslice_optim_min_size
    plt.plot([np.nan] * n, range(n))

