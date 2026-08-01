
def test_std_exception(msg):
    with pytest.raises(RuntimeError) as excinfo:
        m.throw_std_exception()
    assert msg(excinfo.value) == "This exception was intentionally thrown."

