
def test_load_refcount():
    # Check that objects returned by np.load are directly freed based on
    # their refcount, rather than needing the gc to collect them.

    f = BytesIO()
    np.savez(f, [1, 2, 3])
    f.seek(0)

    with assert_no_gc_cycles():
        np.load(f)

    f.seek(0)
    dt = [("a", 'u1', 2), ("b", 'u1', 2)]
    with assert_no_gc_cycles():
        x = np.loadtxt(TextIO("0 1 2 3"), dtype=dt)
        assert_equal(x, np.array([((0, 1), (2, 3))], dtype=dt))

