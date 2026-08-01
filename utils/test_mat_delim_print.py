
def test_mat_delim_print():
    expr = Matrix([[1, 2], [3, 4]])
    assert mathml(expr, printer='presentation', mat_delim='[') == \
        '<mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd>'\
        '<mn>2</mn></mtd></mtr><mtr><mtd><mn>3</mn></mtd><mtd><mn>4</mn>'\
        '</mtd></mtr></mtable><mo>]</mo></mrow>'
    assert mathml(expr, printer='presentation', mat_delim='(') == \
        '<mrow><mo>(</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>2</mn></mtd>'\
        '</mtr><mtr><mtd><mn>3</mn></mtd><mtd><mn>4</mn></mtd></mtr></mtable><mo>)</mo></mrow>'
    assert mathml(expr, printer='presentation', mat_delim='') == \
        '<mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>2</mn></mtd></mtr><mtr>'\
        '<mtd><mn>3</mn></mtd><mtd><mn>4</mn></mtd></mtr></mtable>'

