
def test_wrightomega_inf():
    pts = [complex(np.inf, 10),
           complex(-np.inf, 10),
           complex(10, np.inf),
           complex(10, -np.inf)]
    for p in pts:
        assert_equal(sc.wrightomega(p), p)

