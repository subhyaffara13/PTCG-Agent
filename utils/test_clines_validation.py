
def test_clines_validation(clines, styler):
    msg = f"`clines` value of {clines} is invalid."
    with pytest.raises(ValueError, match=msg):
        styler.to_latex(clines=clines)

