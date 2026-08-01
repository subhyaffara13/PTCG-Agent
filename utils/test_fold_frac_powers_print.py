
def test_fold_frac_powers_print():
    expr = x ** Rational(5, 2)
    assert mathml(expr, printer='presentation') == \
        '<msup><mi>x</mi><mfrac><mn>5</mn><mn>2</mn></mfrac></msup>'
    assert mathml(expr, printer='presentation', fold_frac_powers=True) == \
        '<msup><mi>x</mi><mfrac bevelled="true"><mn>5</mn><mn>2</mn></mfrac></msup>'
    assert mathml(expr, printer='presentation', fold_frac_powers=False) == \
        '<msup><mi>x</mi><mfrac><mn>5</mn><mn>2</mn></mfrac></msup>'

