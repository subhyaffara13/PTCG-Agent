
def test_wrap():
    def assert_references(a, b, base=None):
        if base is None:
            base = a
        assert a is not b
        assert a.__array_interface__["data"][0] == b.__array_interface__["data"][0]
        assert a.shape == b.shape
        assert a.strides == b.strides
        assert a.flags.c_contiguous == b.flags.c_contiguous
        assert a.flags.f_contiguous == b.flags.f_contiguous
        assert a.flags.writeable == b.flags.writeable
        assert a.flags.aligned == b.flags.aligned
        # 1.13 supported Python 3.6
        if tuple(int(x) for x in np.__version__.split(".")[:2]) >= (1, 14):
            assert a.flags.writebackifcopy == b.flags.writebackifcopy
        else:
            assert a.flags.updateifcopy == b.flags.updateifcopy
        assert np.all(a == b)
        assert not b.flags.owndata
        assert b.base is base
        if a.flags.writeable and a.ndim == 2:
            a[0, 0] = 1234
            assert b[0, 0] == 1234

    a1 = np.array([1, 2], dtype=np.int16)
    assert a1.flags.owndata
    assert a1.base is None
    a2 = m.wrap(a1)
    assert_references(a1, a2)

    a1 = np.array([[1, 2], [3, 4]], dtype=np.float32, order="F")
    assert a1.flags.owndata
    assert a1.base is None
    a2 = m.wrap(a1)
    assert_references(a1, a2)

    a1 = np.array([[1, 2], [3, 4]], dtype=np.float32, order="C")
    a1.flags.writeable = False
    a2 = m.wrap(a1)
    assert_references(a1, a2)

    a1 = np.random.random((4, 4, 4))
    a2 = m.wrap(a1)
    assert_references(a1, a2)

    a1t = a1.transpose()
    a2 = m.wrap(a1t)
    assert_references(a1t, a2, a1)

    a1d = a1.diagonal()
    a2 = m.wrap(a1d)
    assert_references(a1d, a2, a1)

    a1m = a1[::-1, ::-1, ::-1]
    a2 = m.wrap(a1m)
    assert_references(a1m, a2, a1)


def test_wrap(any_string_dtype):
    # test values are: two words less than width, two words equal to width,
    # two words greater than width, one word less than width, one word
    # equal to width, one word greater than width, multiple tokens with
    # trailing whitespace equal to width
    s = Series(
        [
            "hello world",
            "hello world!",
            "hello world!!",
            "abcdefabcde",
            "abcdefabcdef",
            "abcdefabcdefa",
            "ab ab ab ab ",
            "ab ab ab ab a",
            "\t",
        ],
        dtype=any_string_dtype,
    )

    # expected values
    expected = Series(
        [
            "hello world",
            "hello world!",
            "hello\nworld!!",
            "abcdefabcde",
            "abcdefabcdef",
            "abcdefabcdef\na",
            "ab ab ab ab",
            "ab ab ab ab\na",
            "",
        ],
        dtype=any_string_dtype,
    )

    result = s.str.wrap(12, break_long_words=True)
    tm.assert_series_equal(result, expected)


def test_wrap(x, rotation, halign):
    fig = plt.figure(figsize=(18, 18))
    gs = GridSpec(nrows=3, ncols=3, figure=fig)
    subfig = fig.add_subfigure(gs[1, 1])
    # we only use the central subfigure, which does not align with any
    # figure boundary, to ensure only subfigure boundaries are relevant
    s = 'This is a very long text that should be wrapped multiple times.'
    text = subfig.text(x, 0.7, s, wrap=True, rotation=rotation, ha=halign)
    fig.canvas.draw()
    assert text._get_wrapped_text() == ('This is a very long\n'
                                        'text that should be\n'
                                        'wrapped multiple\n'
                                        'times.')

