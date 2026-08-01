
def test_rcparams_update():
    rc = mpl.RcParams({'figure.figsize': (3.5, 42)})
    bad_dict = {'figure.figsize': (3.5, 42, 1)}
    # make sure validation happens on input
    with pytest.raises(ValueError):
        rc.update(bad_dict)

