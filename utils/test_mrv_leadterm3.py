
def test_mrv_leadterm3():
    #Gruntz: p56, 3.27
    assert mmrv(exp(-x + exp(-x)*exp(-x*log(x))), x) == {exp(-x - x*log(x))}
    assert mrv_leadterm(exp(-x + exp(-x)*exp(-x*log(x))), x) == (exp(-x), 0)

