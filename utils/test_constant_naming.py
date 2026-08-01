
def test_constant_naming():
    #issue 8697
    assert rsolve(y(n+3) - y(n+2) - y(n+1) + y(n), y(n)) == (-1)**n*C1 + C0 + C2*n
    assert rsolve(y(n+3)+3*y(n+2)+3*y(n+1)+y(n), y(n)).expand() == (-1)**n*C0 - (-1)**n*C1*n - (-1)**n*C2*n**2
    assert rsolve(y(n) - 2*y(n - 3) + 5*y(n - 2) - 4*y(n - 1),y(n),[1,3,8]) == 3*2**n - n - 2

    #issue 19630
    assert rsolve(y(n+3) - 3*y(n+1) + 2*y(n), y(n), {y(1):0, y(2):8, y(3):-2}) == (-2)**n + 2*n

