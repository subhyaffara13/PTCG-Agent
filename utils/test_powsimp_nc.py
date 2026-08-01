
def test_powsimp_nc():
    x, y, z = symbols('x,y,z')
    A, B, C = symbols('A B C', commutative=False)

    assert powsimp(A**x*A**y, combine='all') == A**(x + y)
    assert powsimp(A**x*A**y, combine='base') == A**x*A**y
    assert powsimp(A**x*A**y, combine='exp') == A**(x + y)

    assert powsimp(A**x*B**x, combine='all') == A**x*B**x
    assert powsimp(A**x*B**x, combine='base') == A**x*B**x
    assert powsimp(A**x*B**x, combine='exp') == A**x*B**x

    assert powsimp(B**x*A**x, combine='all') == B**x*A**x
    assert powsimp(B**x*A**x, combine='base') == B**x*A**x
    assert powsimp(B**x*A**x, combine='exp') == B**x*A**x

    assert powsimp(A**x*A**y*A**z, combine='all') == A**(x + y + z)
    assert powsimp(A**x*A**y*A**z, combine='base') == A**x*A**y*A**z
    assert powsimp(A**x*A**y*A**z, combine='exp') == A**(x + y + z)

    assert powsimp(A**x*B**x*C**x, combine='all') == A**x*B**x*C**x
    assert powsimp(A**x*B**x*C**x, combine='base') == A**x*B**x*C**x
    assert powsimp(A**x*B**x*C**x, combine='exp') == A**x*B**x*C**x

    assert powsimp(B**x*A**x*C**x, combine='all') == B**x*A**x*C**x
    assert powsimp(B**x*A**x*C**x, combine='base') == B**x*A**x*C**x
    assert powsimp(B**x*A**x*C**x, combine='exp') == B**x*A**x*C**x

