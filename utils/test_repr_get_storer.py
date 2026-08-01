
def test_repr_get_storer(temp_hdfstore):
    # storers
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )
    temp_hdfstore.append("df", df)

    s = temp_hdfstore.get_storer("df")
    repr(s)
    str(s)

