
def check_vecentropy(distfn, args):
    npt.assert_equal(distfn.vecentropy(*args), distfn._entropy(*args))

