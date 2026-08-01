
def test_roundtrip_simple_cpp_derived():
    p = m.make_SimpleCppDerivedAsBase()
    assert m.check_dynamic_cast_SimpleCppDerived(p)
    p.num = 404
    if not env.PYPY:
        # To ensure that this unit test is not accidentally invalidated.
        with pytest.raises(AttributeError):
            # Mimics the `setstate` C++ implementation.
            setattr(p, "__dict__", {})  # noqa: B010
    data = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
    p2 = pickle.loads(data)
    assert isinstance(p2, m.SimpleBase)
    assert p2.num == 404
    # Issue #3062: pickleable base C++ classes can incur object slicing
    #              if derived typeid is not registered with pybind11
    assert not m.check_dynamic_cast_SimpleCppDerived(p2)

