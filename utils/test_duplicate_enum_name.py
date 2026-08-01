
def test_duplicate_enum_name():
    with pytest.raises(ValueError) as excinfo:
        m.register_bad_enum()
    assert str(excinfo.value) == 'SimpleEnum: element "ONE" already exists!'

