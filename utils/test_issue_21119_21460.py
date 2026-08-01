
def test_issue_21119_21460():
    ss = lambda x: str(S(x, evaluate=False))
    assert ss('4/2') == '4/2'
    assert ss('4/-2') == '4/(-2)'
    assert ss('-4/2') == '-4/2'
    assert ss('-4/-2') == '-4/(-2)'
    assert ss('-2*3/-1') == '-2*3/(-1)'
    assert ss('-2*3/-1/2') == '-2*3/(-1*2)'
    assert ss('4/2/1') == '4/(2*1)'
    assert ss('-2/-1/2') == '-2/(-1*2)'
    assert ss('2*3*4**(-2*3)') == '2*3/4**(2*3)'
    assert ss('2*3*1*4**(-2*3)') == '2*3*1/4**(2*3)'

