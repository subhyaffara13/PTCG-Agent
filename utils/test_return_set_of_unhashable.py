
def test_return_set_of_unhashable():
    with pytest.raises(TypeError) as excinfo:
        m.get_unhashable_HashMe_set()
    assert str(excinfo.value.__cause__).startswith("unhashable type:")

