
def test_log_hp():
    mp.dps = 2000
    a = mpf(10)**15000/3
    r = log(a)
    res = last_digits(r)
    # Mathematica N[Log[10^15000/3], 2000]
    # ...7443804441768333470331
    assert res == '43804441768333470331'

    # see issue 145
    r = log(mpf(3)/2)
    # Mathematica N[Log[3/2], 2000]
    # ...69653749808140753263288
    res = last_digits(r)
    assert res == '53749808140753263288'

    mp.dps = 10000
    r = log(2)
    res = last_digits(r)
    # Mathematica  N[Log[2], 10000]
    # ...695615913401856601359655561
    assert res == '13401856601359655561'
    r = log(mpf(10)**10/3)
    res = last_digits(r)
    # Mathematica N[Log[10^10/3], 10000]
    # ...587087654020631943060007154
    assert res == '54020631943060007154', res
    r = log(mpf(10)**100/3)
    res = last_digits(r)
    # Mathematica N[Log[10^100/3], 10000]
    # ,,,59246336539088351652334666
    assert res == '36539088351652334666', res
    mp.dps += 10
    a = 1 - mpf(1)/10**10
    mp.dps -= 10
    r = log(a)
    res = last_digits(r)
    # ...3310334360482956137216724048322957404
    # 372167240483229574038733026370
    # Mathematica N[Log[1 - 10^-10]*10^10, 10000]
    # ...60482956137216724048322957404
    assert res == '37216724048322957404', res
    mp.dps = 10000
    mp.dps += 100
    a = 1 + mpf(1)/10**100
    mp.dps -= 100

    r = log(a)
    res = last_digits(+r)
    # Mathematica N[Log[1 + 10^-100]*10^10, 10030]
    # ...3994733877377412241546890854692521568292338268273 10^-91
    assert res == '39947338773774122415', res

    mp.dps = 15

