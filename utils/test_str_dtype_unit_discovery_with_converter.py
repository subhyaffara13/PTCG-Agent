
def test_str_dtype_unit_discovery_with_converter():
    data = ["spam-a-lot"] * 60000 + ["XXXtis_but_a_scratch"]
    expected = np.array(
        ["spam-a-lot"] * 60000 + ["tis_but_a_scratch"], dtype="U17"
    )
    conv = lambda s: s.removeprefix("XXX")

    # file-like path
    txt = StringIO("\n".join(data))
    a = np.loadtxt(txt, dtype="U", converters=conv)
    assert a.dtype == expected.dtype
    assert_equal(a, expected)

    # file-obj path
    fd, fname = mkstemp()
    os.close(fd)
    with open(fname, "w") as fh:
        fh.write("\n".join(data))
    a = np.loadtxt(fname, dtype="U", converters=conv)
    os.remove(fname)
    assert a.dtype == expected.dtype
    assert_equal(a, expected)

