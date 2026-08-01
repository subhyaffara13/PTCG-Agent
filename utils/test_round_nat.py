
def test_round_nat(klass, method, freq):
    # see gh-14940
    ts = klass("nat")

    round_method = getattr(ts, method)
    assert round_method(freq) is ts

