
def test_repack_fields() -> None:
    dt: np.dtype[np.void] = np.dtype("u1, <i8, <f8", align=True)

    assert_type(rfn.repack_fields(dt), np.dtype[np.void])
    assert_type(rfn.repack_fields(dt.type(0)), np.void)
    assert_type(
        rfn.repack_fields(np.ones((3,), dtype=dt)),
        np.ndarray[tuple[int], np.dtype[np.void]],
    )

