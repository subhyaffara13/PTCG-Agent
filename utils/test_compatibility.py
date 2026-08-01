
def test_compatibility(freqstr, expected):
    ts_np = np.datetime64("2021-01-01T08:00:00.00")
    do = to_offset(freqstr)
    assert ts_np + do == np.datetime64(expected)


def test_compatibility():
    try:
        import numpy as np
        from fractions import Fraction
        from decimal import Decimal
        import decimal
    except ImportError:
        return
    # numpy types
    for nptype in np.core.numerictypes.typeDict.values():
        if issubclass(nptype, np.complexfloating):
            x = nptype(complex(0.5, -0.5))
        elif issubclass(nptype, np.floating):
            x = nptype(0.5)
        elif issubclass(nptype, np.integer):
            x = nptype(2)
        # Handle the weird types
        try: diff = np.abs(type(np.sqrt(x))(sqrt(x)) - np.sqrt(x))
        except: continue
        assert diff < 2.0**-53
    #Fraction and Decimal
    oldprec = mp.prec
    mp.prec = 1000
    decimal.getcontext().prec = mp.dps
    assert sqrt(Fraction(2, 3)).ae(sqrt(mpf('2/3')))
    assert sqrt(Decimal(2)/Decimal(3)).ae(sqrt(mpf('2/3')))
    mp.prec = oldprec

