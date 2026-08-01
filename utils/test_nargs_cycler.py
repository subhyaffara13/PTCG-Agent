
def test_nargs_cycler():
    from matplotlib.rcsetup import cycler as ccl
    with pytest.raises(TypeError, match='3 were given'):
        # cycler() takes 0-2 arguments.
        ccl(ccl(color=list('rgb')), 2, 3)

