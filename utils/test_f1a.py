
def test_f1a():
    #issue 3508:
    assert limit((sin(2*x)/x)**(1 + x), x, 0) == 2  # Primer 7

