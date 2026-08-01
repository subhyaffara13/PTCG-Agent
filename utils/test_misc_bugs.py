
def test_misc_bugs():
    # test that this doesn't raise an exception
    mp.dps = 1000
    log(1302)
    mp.dps = 15

