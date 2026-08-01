
def test_bisection():
    # issue 273
    assert findroot(lambda x: x**2-1,(0,2),solver='bisect') == 1

