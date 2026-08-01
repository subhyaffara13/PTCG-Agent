
def test_dsolve_ics():
    # Maybe this should just use one of the solutions instead of raising...
    with raises(NotImplementedError):
        dsolve(f(x).diff(x) - sqrt(f(x)), ics={f(1):1})

