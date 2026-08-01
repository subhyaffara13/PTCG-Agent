
def test_sinc_opts():
    def check(d):
        for k, v in d.items():
            assert optimize(k, sinc_opts) == v

    x = Symbol('x')
    check({
        sin(x)/x       : sinc(x),
        sin(2*x)/(2*x) : sinc(2*x),
        sin(3*x)/x     : 3*sinc(3*x),
        x*sin(x)       : x*sin(x)
    })

    y = Symbol('y')
    check({
        sin(x*y)/(x*y)       : sinc(x*y),
        y*sin(x/y)/x         : sinc(x/y),
        sin(sin(x))/sin(x)   : sinc(sin(x)),
        sin(3*sin(x))/sin(x) : 3*sinc(3*sin(x)),
        sin(x)/y             : sin(x)/y
    })

