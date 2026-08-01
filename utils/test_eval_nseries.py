
def test_eval_nseries():
    a1, b1, a2, b2 = symbols('a1 b1 a2 b2')
    assert hyper((1,2), (1,2,3), x**2)._eval_nseries(x, 7, None) == \
        1 + x**2/3 + x**4/24 + x**6/360 + O(x**7)
    assert exp(x)._eval_nseries(x,7,None) == \
        hyper((a1, b1), (a1, b1), x)._eval_nseries(x, 7, None)
    assert hyper((a1, a2), (b1, b2), x)._eval_nseries(z, 7, None) ==\
        hyper((a1, a2), (b1, b2), x) + O(z**7)
    assert hyper((-S(1)/2, S(1)/2), (1,), 4*x/(x + 1)).nseries(x) == \
        1 - x + x**2/4 - 3*x**3/4 - 15*x**4/64 - 93*x**5/64 + O(x**6)
    assert (pi/2*hyper((-S(1)/2, S(1)/2), (1,), 4*x/(x + 1))).nseries(x) == \
        pi/2 - pi*x/2 + pi*x**2/8 - 3*pi*x**3/8 - 15*pi*x**4/128 - 93*pi*x**5/128 + O(x**6)

