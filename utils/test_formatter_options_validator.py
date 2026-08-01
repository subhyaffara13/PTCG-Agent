
def test_formatter_options_validator(formatter, exp):
    df = DataFrame([[9]])
    with option_context("styler.format.formatter", formatter):
        assert f" {exp} " in df.style.to_latex()

