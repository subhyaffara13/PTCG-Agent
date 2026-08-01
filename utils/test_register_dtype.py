
def test_register_dtype():
    with pytest.raises(RuntimeError) as excinfo:
        m.register_dtype()
    assert "dtype is already registered" in str(excinfo.value)

