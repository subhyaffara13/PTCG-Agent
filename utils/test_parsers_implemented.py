
def test_parsers_implemented():
    with pytest.raises(NotImplementedError):
        handler = ErrConfigHandler(None, {}, False, Mock())
        handler.parsers

