
def test_presentation_mathml_disable_split_super_sub():
    mpp = MathMLPresentationPrinter()
    assert mpp.doprint(Symbol('u_b')) == '<msub><mi>u</mi><mi>b</mi></msub>'
    mpp = MathMLPresentationPrinter({'disable_split_super_sub': False})
    assert mpp.doprint(Symbol('u_b')) == '<msub><mi>u</mi><mi>b</mi></msub>'
    mpp = MathMLPresentationPrinter({'disable_split_super_sub': True})
    assert mpp.doprint(Symbol('u_b')) == '<mi>u_b</mi>'

