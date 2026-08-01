
def test_gh14467():
    # gh-14467 noted that some physical constants in CODATA are rounded
    # to only ten significant figures even though they are supposed to be
    # exact. Check that (at least) the case mentioned in the issue is resolved.
    res = constants.physical_constants['Boltzmann constant in eV/K'][0]
    ref = (constants.physical_constants['Boltzmann constant'][0]
           / constants.physical_constants['elementary charge'][0])
    assert res == ref

