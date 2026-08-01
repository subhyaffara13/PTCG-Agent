
def test_raise_from_already_set(msg):
    with pytest.raises(ValueError) as excinfo:
        m.raise_from_already_set()
    assert msg(excinfo.value) == "outer"
    assert msg(excinfo.value.__cause__) == "inner"

