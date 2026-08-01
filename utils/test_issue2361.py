
def test_issue2361():
    # See issue #2361
    assert m.issue2361_str_implicit_copy_none() == "None"
    with pytest.raises(TypeError) as excinfo:
        assert m.issue2361_dict_implicit_copy_none()
    assert "NoneType" in str(excinfo.value)
    assert "iterable" in str(excinfo.value)

