
def test_print_conjugate():
    assert mpp.doprint(conjugate(x)) == \
        '<menclose notation="top"><mi>x</mi></menclose>'
    assert mpp.doprint(conjugate(x + 1)) == \
        '<mrow><menclose notation="top"><mi>x</mi></menclose><mo>+</mo><mn>1</mn></mrow>'

