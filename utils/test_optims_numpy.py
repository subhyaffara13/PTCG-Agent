
def test_optims_numpy():
    def check(d):
        for k, v in d.items():
            assert optimize(k, optims_numpy) == v

    x = Symbol('x')
    check({
        sin(2*x)/(2*x) + exp(2*x) - 1: sinc(2*x) + expm1(2*x),
        log(x+3)/log(2) + log(x**2 + 1): log1p(x**2) + log2(x+3)
    })

