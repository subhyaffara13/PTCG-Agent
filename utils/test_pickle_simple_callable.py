
def test_pickle_simple_callable():
    assert m.simple_callable() == 20220426
    if env.PYPY:
        serialized = pickle.dumps(m.simple_callable)
        deserialized = pickle.loads(serialized)
        assert deserialized() == 20220426
    else:
        # To document broken behavior: currently it fails universally with
        # all C Python versions.
        with pytest.raises(TypeError) as excinfo:
            pickle.dumps(m.simple_callable)
        assert re.search("can.*t pickle .*PyCapsule.* object", str(excinfo.value))

