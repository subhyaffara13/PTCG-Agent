
def test_option_context_invalid_option():
    with pytest.raises(OptionError, match="No such keys"):
        with cf.option_context("invalid", True):
            pass

