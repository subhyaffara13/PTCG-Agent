
def test_Pow_as_content_primitive():
    assert (x**y).as_content_primitive() == (1, x**y)
    assert ((2*x + 2)**y).as_content_primitive() == \
        (1, (Mul(2, (x + 1), evaluate=False))**y)
    assert ((2*x + 2)**3).as_content_primitive() == (8, (x + 1)**3)

