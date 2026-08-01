
def test_optims_numpy_TODO():
    def check(d):
        for k, v in d.items():
            assert optimize(k, optims_numpy) == v

    x, y = map(Symbol, 'x y'.split())
    check({
        log(x*y)*sin(x*y)*log(x*y+1)/(log(2)*x*y): log2(x*y)*sinc(x*y)*log1p(x*y),
        exp(x*sin(y)/y) - 1: expm1(x*sinc(y))
    })

