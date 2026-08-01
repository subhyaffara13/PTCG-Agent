
def test_throw_nested_exception():
    with pytest.raises(RuntimeError) as excinfo:
        m.throw_nested_exception()
    assert str(excinfo.value) == "Outer Exception"
    assert str(excinfo.value.__cause__) == "Inner Exception"

