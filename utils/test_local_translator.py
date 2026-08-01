
def test_local_translator(msg):
    """Tests that a local translator works and that the local translator from
    the cross module is not applied"""
    with pytest.raises(RuntimeError) as excinfo:
        m.throws6()
    assert msg(excinfo.value) == "MyException6 only handled in this module"

    with pytest.raises(RuntimeError) as excinfo:
        m.throws_local_error()
    assert not isinstance(excinfo.value, KeyError)
    assert msg(excinfo.value) == "never caught"

    with pytest.raises(Exception) as excinfo:
        m.throws_local_simple_error()
    assert not isinstance(excinfo.value, cm.LocalSimpleException)
    assert msg(excinfo.value) == "this mod"

