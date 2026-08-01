
def test_wrightomega_nan():
    pts = [complex(np.nan, 0),
           complex(0, np.nan),
           complex(np.nan, np.nan),
           complex(np.nan, 1),
           complex(1, np.nan)]
    for p in pts:
        res = sc.wrightomega(p)
        assert_(np.isnan(res.real))
        assert_(np.isnan(res.imag))

