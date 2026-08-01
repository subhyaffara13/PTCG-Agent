
def test_iterator(doc):
    assert doc(m.get_iterator) == "get_iterator() -> Iterator"


def test_iterator():
    array = ImmutableDenseNDimArray(range(4), (2, 2))
    assert array[0] == ImmutableDenseNDimArray([0, 1])
    assert array[1] == ImmutableDenseNDimArray([2, 3])

    array = array.reshape(4)
    j = 0
    for i in array:
        assert i == j
        j += 1


def test_iterator():
    array = MutableDenseNDimArray(range(4), (2, 2))
    assert array[0] == MutableDenseNDimArray([0, 1])
    assert array[1] == MutableDenseNDimArray([2, 3])

    array = array.reshape(4)
    j = 0
    for i in array:
        assert i == j
        j += 1


def test_iterator(all_parsers):
    # see gh-6607
    data = """index,A,B,C,D
foo,2,3,4,5
bar,7,8,9,10
baz,12,13,14,15
qux,12,13,14,15
foo2,12,13,14,15
bar2,12,13,14,15
"""
    parser = all_parsers
    kwargs = {"index_col": 0}

    expected = parser.read_csv(StringIO(data), **kwargs)

    if parser.engine == "pyarrow":
        msg = "The 'iterator' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), iterator=True, **kwargs)
        return

    with parser.read_csv(StringIO(data), iterator=True, **kwargs) as reader:
        first_chunk = reader.read(3)
        tm.assert_frame_equal(first_chunk, expected[:3])

        last_chunk = reader.read(5)
    tm.assert_frame_equal(last_chunk, expected[3:])

