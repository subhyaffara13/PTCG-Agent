
def test_cast_object_to_pyobject_ptr():
    assert m.cast_object_to_pyobject_ptr(ValueHolder(43)) == 257

