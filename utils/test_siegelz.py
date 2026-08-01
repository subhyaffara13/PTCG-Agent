
def test_siegelz():
    mp.dps = 15
    assert siegelz(100000).ae(5.87959246868176504171)
    assert siegelz(100000, derivative=2).ae(-54.1172711010126452832)
    assert siegelz(100000, derivative=3).ae(-278.930831343966552538)
    assert siegelz(100000+j,derivative=1).ae(678.214511857070283307-379.742160779916375413j)

