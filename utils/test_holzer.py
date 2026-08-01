
def test_holzer():
    # if the input is good, don't let it diverge in holzer()
    # (but see test_fail_holzer below)
    assert holzer(2, 7, 13, 4, 79, 23) == (2, 7, 13)

    # None in uv condition met; solution is not Holzer reduced
    # so this will hopefully change but is here for coverage
    assert holzer(2, 6, 2, 1, 1, 10) == (2, 6, 2)

    raises(ValueError, lambda: holzer(2, 7, 14, 4, 79, 23))

