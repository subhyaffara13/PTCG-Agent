
def test_bool_options(styler, option):
    with option_context(f"styler.latex.{option}", False):
        latex_false = styler.to_latex()
    with option_context(f"styler.latex.{option}", True):
        latex_true = styler.to_latex()
    assert latex_false != latex_true  # options are reactive under to_latex(*no_args)

