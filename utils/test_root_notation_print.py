
def test_root_notation_print():
    assert mathml(x**(S.One/3), printer='presentation') == \
        '<mroot><mi>x</mi><mn>3</mn></mroot>'
    assert mathml(x**(S.One/3), printer='presentation', root_notation=False) ==\
        '<msup><mi>x</mi><mfrac><mn>1</mn><mn>3</mn></mfrac></msup>'
    assert mathml(x**(S.One/3), printer='content') == \
        '<apply><root/><degree><cn>3</cn></degree><ci>x</ci></apply>'
    assert mathml(x**(S.One/3), printer='content', root_notation=False) == \
        '<apply><power/><ci>x</ci><apply><divide/><cn>1</cn><cn>3</cn></apply></apply>'
    assert mathml(x**(Rational(-1, 3)), printer='presentation') == \
        '<mfrac><mn>1</mn><mroot><mi>x</mi><mn>3</mn></mroot></mfrac>'
    assert mathml(x**(Rational(-1, 3)), printer='presentation', root_notation=False) \
        == '<mfrac><mn>1</mn><msup><mi>x</mi><mfrac><mn>1</mn><mn>3</mn></mfrac></msup></mfrac>'

