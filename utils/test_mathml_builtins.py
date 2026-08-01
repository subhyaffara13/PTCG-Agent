
def test_mathml_builtins():
    assert mpp.doprint(None) == '<mi>None</mi>'
    assert mpp.doprint(true) == '<mi>True</mi>'
    assert mpp.doprint(false) == '<mi>False</mi>'

