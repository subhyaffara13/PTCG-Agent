
def test_issue_438():
    assert mpf(finf) == mpf('inf')
    assert mpf(fninf) == mpf('-inf')
    assert mpf(fnan)._mpf_ == mpf('nan')._mpf_

