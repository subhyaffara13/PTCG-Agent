
def test_get_names_flat() -> None:
    names: tuple[str, ...]
    names = rfn.get_names_flat(np.empty((1,), dtype=[("A", int)]).dtype)
    names = rfn.get_names_flat(np.empty((1,), dtype=[("A", int), ("B", float)]).dtype)

    adtype = np.dtype([("a", int), ("b", [("b_a", int), ("b_b", int)])])
    names = rfn.get_names_flat(adtype)

