
def test_print_Float():
    assert mpp.doprint(Float(1e100)) == '<mrow><mn>1.0</mn><mo>&#xB7;</mo><msup><mn>10</mn><mn>100</mn></msup></mrow>'
    assert mpp.doprint(Float(1e-100)) == '<mrow><mn>1.0</mn><mo>&#xB7;</mo><msup><mn>10</mn><mn>-100</mn></msup></mrow>'
    assert mpp.doprint(Float(-1e100)) == '<mrow><mn>-1.0</mn><mo>&#xB7;</mo><msup><mn>10</mn><mn>100</mn></msup></mrow>'
    assert mpp.doprint(Float(1.0*oo)) == '<mi>&#x221E;</mi>'
    assert mpp.doprint(Float(-1.0*oo)) == '<mrow><mo>-</mo><mi>&#x221E;</mi></mrow>'

