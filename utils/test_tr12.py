
def test_TR12():
    assert TR12(tan(x + y)) == (tan(x) + tan(y))/(-tan(x)*tan(y) + 1)
    assert TR12(tan(x + y + z)) ==\
        (tan(z) + (tan(x) + tan(y))/(-tan(x)*tan(y) + 1))/(
        1 - (tan(x) + tan(y))*tan(z)/(-tan(x)*tan(y) + 1))
    assert TR12(tan(x*y)) == tan(x*y)

