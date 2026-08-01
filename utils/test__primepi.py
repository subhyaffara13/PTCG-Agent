
def test__primepi():
    assert _primepi(-1) == 0
    assert _primepi(1) == 0
    assert _primepi(2) == 1
    assert _primepi(5) == 3
    assert _primepi(11) == 5
    assert _primepi(57) == 16
    assert _primepi(296) == 62
    assert _primepi(559) == 102
    assert _primepi(3000) == 430
    assert _primepi(4096) == 564
    assert _primepi(9096) == 1128
    assert _primepi(25023) == 2763
    assert _primepi(10**8) == 5761455
    assert _primepi(253425253) == 13856396
    assert _primepi(8769575643) == 401464322
    sieve.extend(3000)
    assert _primepi(2000) == 303

