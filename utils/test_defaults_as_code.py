
def test_defaults_as_code():
    for param in rcsetup._params_list():
        if param.name == 'backend':
            # backend has special handling and no meaningful default
            continue
        assert param.default == mpl.rcParamsDefault[param.name], param.name

