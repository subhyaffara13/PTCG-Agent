
def test_interval_matrix():
    mp.dps = 15
    iv.dps = 15
    a = iv.matrix([['0.1','0.3','1.0'],['7.1','5.5','4.8'],['3.2','4.4','5.6']])
    b = iv.matrix(['4','0.6','0.5'])
    c = iv.lu_solve(a, b)
    assert c[0].delta < 1e-13
    assert c[1].delta < 1e-13
    assert c[2].delta < 1e-13
    assert 5.25823271130625686059275 in c[0]
    assert -13.155049396267837541163 in c[1]
    assert 7.42069154774972557628979 in c[2]

