
def test_trigsimp2():
    x, y = symbols('x,y')
    assert trigsimp(cos(x)**2*sin(y)**2 + cos(x)**2*cos(y)**2 + sin(x)**2,
            recursive=True) == 1
    assert trigsimp(sin(x)**2*sin(y)**2 + sin(x)**2*cos(y)**2 + cos(x)**2,
            recursive=True) == 1
    assert trigsimp(
        Subs(x, x, sin(y)**2 + cos(y)**2)) == Subs(x, x, 1)

