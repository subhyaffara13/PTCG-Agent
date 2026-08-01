
def test_is_reduced():
    R, x, y = ring("x,y", QQ, lex)
    f = x**2 + 2*x*y**2
    g = x*y + 2*y**3 - 1
    assert is_reduced([f, g], R) ==  False
    G = groebner([f, g], R)
    assert is_reduced(G, R) == True

