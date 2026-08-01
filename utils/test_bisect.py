
def test_bisect():
    npt.assert_allclose(
        EXPECTED,
        list(
            _zeros.loop_example('bisect', A0, ARGS, XLO, XHI, XTOL, RTOL, MITR)
        ),
        rtol=RTOL, atol=XTOL
    )

