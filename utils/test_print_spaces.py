
def test_print_spaces():
    assert mpp.doprint(HilbertSpace()) == '<mi>&#x210B;</mi>'
    assert mpp.doprint(ComplexSpace(2)) == '<msup>&#x1D49E;<mn>2</mn></msup>'
    assert mpp.doprint(FockSpace()) == '<mi>&#x2131;</mi>'

