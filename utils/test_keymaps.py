
def test_keymaps():
    key_list = [k for k in mpl.rcParams if 'keymap' in k]
    for k in key_list:
        assert isinstance(mpl.rcParams[k], list)

