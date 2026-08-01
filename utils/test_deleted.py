
def test_deleted():
    global sin
    from dill import dumps, loads
    from math import sin, pi

    def sinc(x):
        return sin(x)/x

    settings['recurse'] = True
    _sinc = dumps(sinc)
    sin = globals().pop('sin')
    sin = 1
    del sin
    sinc_ = loads(_sinc) # no NameError... pickling preserves 'sin'
    res = sinc_(1)
    from math import sin
    assert sinc(1) == res

