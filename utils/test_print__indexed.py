
def test_print_Indexed():
    assert mathml(IndexedBase(a), printer='presentation') == '<mi>a</mi>'
    assert mathml(IndexedBase(a/b), printer='presentation') == \
        '<mrow><mfrac><mi>a</mi><mi>b</mi></mfrac></mrow>'
    assert mathml(IndexedBase((a, b)), printer='presentation') == \
        '<mrow><mo>(</mo><mi>a</mi><mo>,</mo><mi>b</mi><mo>)</mo></mrow>'

