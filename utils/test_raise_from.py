
def test_raise_from(msg):
    with pytest.raises(ValueError) as excinfo:
        m.raise_from()
    assert msg(excinfo.value) == "outer"
    assert msg(excinfo.value.__cause__) == "inner"

