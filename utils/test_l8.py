
def test_L8():
    assert simplify((4*x + 4*sqrt(x) + 1)**(sqrt(x)/(2*sqrt(x) + 1)) \
        *(2*sqrt(x) + 1)**(1/(2*sqrt(x) + 1)) - 2*sqrt(x) - 1) == 0

