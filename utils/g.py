
def g(a, b=0, c=0, d=0):
    with tm.assert_produces_warning(None):
        return a + b + c + d


def g(a, b, c=2):  # with keywords
    pass


def g(x): return f(x) - x


def g(x): return f(x) - x


def g(x): return f(x) - x

