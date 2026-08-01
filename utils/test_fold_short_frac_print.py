
def test_fold_short_frac_print():
    expr = Rational(2, 5)
    assert mathml(expr, printer='presentation') == \
        '<mfrac><mn>2</mn><mn>5</mn></mfrac>'
    assert mathml(expr, printer='presentation', fold_short_frac=True) == \
        '<mfrac bevelled="true"><mn>2</mn><mn>5</mn></mfrac>'
    assert mathml(expr, printer='presentation', fold_short_frac=False) == \
        '<mfrac><mn>2</mn><mn>5</mn></mfrac>'

