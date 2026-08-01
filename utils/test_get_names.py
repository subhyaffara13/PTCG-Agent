
def test_get_names() -> None:
    names: tuple[str | Any, ...]
    names = rfn.get_names(np.empty((1,), dtype=[("A", int)]).dtype)
    names = rfn.get_names(np.empty((1,), dtype=[("A", int), ("B", float)]).dtype)

    adtype = np.dtype([("a", int), ("b", [("b_a", int), ("b_b", int)])])
    names = rfn.get_names(adtype)

