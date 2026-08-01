
def test_find_duplicates() -> None:
    ndtype = np.dtype([("a", int)])

    a = np.ma.ones(7).view(ndtype)
    assert_type(
        rfn.find_duplicates(a),
        np.ma.MaskedArray[tuple[int], np.dtype[np.void]],
    )
    assert_type(
        rfn.find_duplicates(a, ignoremask=True, return_index=True),
        tuple[
            np.ma.MaskedArray[tuple[int], np.dtype[np.void]],
            np.ndarray[tuple[int], np.dtype[np.int_]],
        ],
    )

