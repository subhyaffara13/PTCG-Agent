
def test_all_params_defined_as_code():
    assert set(p.name for p in rcsetup._params_list()) == set(mpl.rcParams.keys())

