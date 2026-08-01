
def test_sieve_iter():
    values = []
    for value in sieve:
        if value > 7:
            break
        values.append(value)
    assert values == list(sieve[1:5])

