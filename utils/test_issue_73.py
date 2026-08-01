
def test_issue_73():
    mp.dps = 512
    a = exp(-1)
    b = exp(1)
    mp.dps = 15
    assert (+a).ae(0.36787944117144233)
    assert (+b).ae(2.7182818284590451)

