
def test_div_300():

    q = fi(1000000)
    a = fi(300499999)    # a/q is a little less than a half-integer
    b = fi(300500000)    # b/q exactly a half-integer
    c = fi(300500001)    # c/q is a little more than a half-integer

    # Check nearest integer rounding (prec=9 as 2**8 < 300 < 2**9)

    assert mpf_div(a, q, 9, round_down) == fi(300)
    assert mpf_div(b, q, 9, round_down) == fi(300)
    assert mpf_div(c, q, 9, round_down) == fi(300)
    assert mpf_div(a, q, 9, round_up) == fi(301)
    assert mpf_div(b, q, 9, round_up) == fi(301)
    assert mpf_div(c, q, 9, round_up) == fi(301)

    # Nearest even integer is down
    assert mpf_div(a, q, 9, round_nearest) == fi(300)
    assert mpf_div(b, q, 9, round_nearest) == fi(300)
    assert mpf_div(c, q, 9, round_nearest) == fi(301)

    # Nearest even integer is up
    a = fi(301499999)
    b = fi(301500000)
    c = fi(301500001)
    assert mpf_div(a, q, 9, round_nearest) == fi(301)
    assert mpf_div(b, q, 9, round_nearest) == fi(302)
    assert mpf_div(c, q, 9, round_nearest) == fi(302)

