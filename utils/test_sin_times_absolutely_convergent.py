
def test_sin_times_absolutely_convergent():
    assert Sum(sin(n) / n**3, (n, 1, oo)).is_convergent() is S.true
    assert Sum(sin(n) * log(n) / n**3, (n, 1, oo)).is_convergent() is S.true

