
def test_bad_locator_subs(sub):
    ll = mticker.LogLocator()
    with pytest.raises(ValueError):
        ll.set_params(subs=sub)

