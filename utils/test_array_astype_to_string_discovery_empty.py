
def test_array_astype_to_string_discovery_empty(dt):
    # See also gh-19085
    arr = np.array([""], dtype=object)
    # Note, the itemsize is the `0 -> 1` logic, which should change.
    # The important part the test is rather that it does not error.
    assert arr.astype(dt).dtype.itemsize == np.dtype(f"{dt}1").itemsize

    # check the same thing for `np.can_cast` (since it accepts arrays)
    assert np.can_cast(arr, dt, casting="unsafe")
    assert not np.can_cast(arr, dt, casting="same_kind")
    # as well as for the object as a descriptor:
    assert np.can_cast("O", dt, casting="unsafe")

