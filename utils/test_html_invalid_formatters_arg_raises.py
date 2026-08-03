import re

def test_html_invalid_formatters_arg_raises(size):
    # issue-28469
    df = DataFrame(columns=["a", "b", "c"])
    msg = "Formatters length({}) should match DataFrame number of columns(3)"
    with pytest.raises(ValueError, match=re.escape(msg.format(size))):
        df.to_html(formatters=["{}".format] * size)

