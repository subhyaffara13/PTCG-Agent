
def test_rc_aliases(group, option, alias, value):
    rc_kwargs = {alias: value,}
    mpl.rc(group, **rc_kwargs)

    rcParams_key = f"{group}.{option}"
    assert mpl.rcParams[rcParams_key] == value

