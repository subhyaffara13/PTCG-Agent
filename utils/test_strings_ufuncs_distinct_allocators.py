
def test_strings_ufuncs_distinct_allocators():
    n = 50
    a_list = [f"{'AB' * 10}{i:06d}" for i in range(n)]
    # equal to a in every other entry, all arena strings
    b_list = [s if i % 2 else s[:-1] + "Z" for i, s in enumerate(a_list)]
    a = np.array(a_list, dtype="T")
    b = np.array(b_list, dtype="T")
    assert a.dtype is not b.dtype
    au = a.astype("U40")
    bu = b.astype("U40")

    expected = np.add(np.array(a_list, dtype=object),
                      np.array(b_list, dtype=object))
    assert_array_equal(np.add(a, b), expected)
    out = np.empty(n, dtype="T")
    np.add(a, b, out=out)
    assert_array_equal(out, expected)

    for op in [
        np.equal, np.not_equal, np.less, np.less_equal, np.greater,
        np.greater_equal,
    ]:
        assert_array_equal(op(a, b), op(au, bu))

    # no fixed-width unicode loops for maximum/minimum, so use object
    a_obj = np.array(a_list, dtype=object)
    b_obj = np.array(b_list, dtype=object)
    assert_array_equal(np.maximum(a, b), np.maximum(a_obj, b_obj))
    assert_array_equal(np.minimum(a, b), np.minimum(a_obj, b_obj))
    np.maximum(a, b, out=out)
    assert_array_equal(out, np.maximum(a_obj, b_obj))

    # needles long enough to live in the arena, found in half the entries
    needles_list = [
        a_list[i][:16] if i % 3 else "Z" * 16 for i in range(n)
    ]
    needles = np.array(needles_list, dtype="T")
    needles_u = needles.astype("U20")
    for func in [
        np.strings.find, np.strings.count, np.strings.startswith,
        np.strings.endswith,
    ]:
        assert_array_equal(func(a, needles), func(au, needles_u))

    # three distinct instances feeding one ufunc
    old = np.array(["AB" * 8] * n, dtype="T")
    new = np.array(["xy" * 9] * n, dtype="T")
    assert_array_equal(
        np.strings.replace(a, old, new),
        np.strings.replace(au, old.astype("U16"), new.astype("U18")),
    )

    chars = np.array(["BA0123456789" + "C" * 8] * n, dtype="T")
    assert_array_equal(
        np.strings.strip(a, chars), np.strings.strip(au, chars.astype("U20"))
    )

    sep = np.array(["AB" * 8] * n, dtype="T")
    for part, part_u in zip(
        np.strings.partition(a, sep),
        np.strings.partition(au, sep.astype("U16")),
    ):
        assert_array_equal(part, part_u)

