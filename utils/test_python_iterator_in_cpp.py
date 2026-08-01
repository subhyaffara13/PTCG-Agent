
def test_python_iterator_in_cpp():
    t = (1, 2, 3)
    assert m.object_to_list(t) == [1, 2, 3]
    assert m.object_to_list(iter(t)) == [1, 2, 3]
    assert m.iterator_to_list(iter(t)) == [1, 2, 3]

    with pytest.raises(TypeError) as excinfo:
        m.object_to_list(1)
    assert "object is not iterable" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        m.iterator_to_list(1)
    assert "incompatible function arguments" in str(excinfo.value)

    def bad_next_call():
        raise RuntimeError("py::iterator::advance() should propagate errors")

    with pytest.raises(RuntimeError) as excinfo:
        m.iterator_to_list(iter(bad_next_call, None))
    assert str(excinfo.value) == "py::iterator::advance() should propagate errors"

    lst = [1, None, 0, None]
    assert m.count_none(lst) == 2
    assert m.find_none(lst) is True
    assert m.count_nonzeros({"a": 0, "b": 1, "c": 2}) == 2

    r = range(5)
    assert all(m.tuple_iterator(tuple(r)))
    assert all(m.list_iterator(list(r)))
    assert all(m.sequence_iterator(r))

