
def test_print_Determinant():
    assert mpp.doprint(Determinant(Matrix([[1, 2], [3, 4]]))) == \
        '<mrow><mo>|</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mn>3</mn></mtd><mtd><mn>4</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>|</mo></mrow>'

