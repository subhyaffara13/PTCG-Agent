
def test_fn_cast_int_exception():
    with pytest.raises(RuntimeError) as excinfo:
        m.test_fn_cast_int(lambda: None)

    assert str(excinfo.value).startswith(
        "Unable to cast Python instance of type <class 'NoneType'> to C++ type"
    )

