
def test_environment_option(styler):
    with option_context("styler.latex.environment", "bar-env"):
        assert "\\begin{bar-env}" in styler.to_latex()
        assert "\\begin{foo-env}" in styler.to_latex(environment="foo-env")

