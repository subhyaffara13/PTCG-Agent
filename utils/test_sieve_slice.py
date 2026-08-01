
def test_sieve_slice():
    assert sieve[5] == 11
    assert list(sieve[5:10]) == [sieve[x] for x in range(5, 10)]
    assert list(sieve[5:10:2]) == [sieve[x] for x in range(5, 10, 2)]
    assert list(sieve[1:5]) == [2, 3, 5, 7]
    raises(IndexError, lambda: sieve[:5])
    raises(IndexError, lambda: sieve[0])
    raises(IndexError, lambda: sieve[0:5])

