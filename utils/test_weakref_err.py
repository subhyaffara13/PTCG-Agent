
def test_weakref_err(create_weakref, has_callback):
    class C:
        __slots__ = []

    def callback(_):
        pass

    ob = C()
    # Should raise TypeError on CPython
    with pytest.raises(TypeError) if not env.PYPY else contextlib.nullcontext():
        _ = create_weakref(ob, callback) if has_callback else create_weakref(ob)

