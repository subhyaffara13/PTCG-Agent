
def test_rcparams_init():
    with pytest.raises(ValueError):
        mpl.RcParams({'figure.figsize': (3.5, 42, 1)})

