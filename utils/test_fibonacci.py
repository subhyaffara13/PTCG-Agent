
def test_fibonacci():
    assert [fibonacci(n) for n in range(-3, 5)] == [2, -1, 1, 0, 1, 1, 2, 3]
    assert fibonacci(100) == 354224848179261915075
    assert [lucas(n) for n in range(-3, 5)] == [-4, 3, -1, 2, 1, 3, 4, 7]
    assert lucas(100) == 792070839848372253127

    assert fibonacci(1, x) == 1
    assert fibonacci(2, x) == x
    assert fibonacci(3, x) == x**2 + 1
    assert fibonacci(4, x) == x**3 + 2*x

    # issue #8800
    n = Dummy('n')
    assert fibonacci(n).limit(n, S.Infinity) is S.Infinity
    assert lucas(n).limit(n, S.Infinity) is S.Infinity

    assert fibonacci(n).rewrite(sqrt) == \
        2**(-n)*sqrt(5)*((1 + sqrt(5))**n - (-sqrt(5) + 1)**n) / 5
    assert fibonacci(n).rewrite(sqrt).subs(n, 10).expand() == fibonacci(10)
    assert fibonacci(n).rewrite(GoldenRatio).subs(n,10).evalf() == \
        Float(fibonacci(10))
    assert lucas(n).rewrite(sqrt) == \
        (fibonacci(n-1).rewrite(sqrt) + fibonacci(n+1).rewrite(sqrt)).simplify()
    assert lucas(n).rewrite(sqrt).subs(n, 10).expand() == lucas(10)
    raises(ValueError, lambda: fibonacci(-3, x))


def test_fibonacci():
    mp.dps = 15
    assert [fibonacci(n) for n in range(-5, 10)] == \
        [5, -3, 2, -1, 1, 0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert fib(2.5).ae(1.4893065462657091)
    assert fib(3+4j).ae(-5248.51130728372 - 14195.962288353j)
    assert fib(1000).ae(4.3466557686937455e+208)
    assert str(fib(10**100)) == '6.24499112864607e+2089876402499787337692720892375554168224592399182109535392875613974104853496745963277658556235103534'
    mp.dps = 2100
    a = fib(10000)
    assert a % 10**10 == 9947366875
    mp.dps = 15
    assert fibonacci(inf) == inf
    assert fib(3+0j) == 2

