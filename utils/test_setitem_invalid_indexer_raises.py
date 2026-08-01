
def test_setitem_invalid_indexer_raises():
    pa = pytest.importorskip("pyarrow")

    arr = ArrowStringArray(pa.array(list("abcde")))

    with tm.external_error_raised(IndexError):
        arr[5] = "foo"

    with tm.external_error_raised(IndexError):
        arr[-6] = "foo"

    with tm.external_error_raised(IndexError):
        arr[[0, 5]] = "foo"

    with tm.external_error_raised(IndexError):
        arr[[0, -6]] = "foo"

    with tm.external_error_raised(IndexError):
        arr[[True, True, False]] = "foo"

    with tm.external_error_raised(ValueError):
        arr[[0, 1]] = ["foo", "bar", "baz"]

