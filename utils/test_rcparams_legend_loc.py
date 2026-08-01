
def test_rcparams_legend_loc(value):
    # rcParams['legend.loc'] should allow any of the following formats.
    # if any of these are not allowed, an exception will be raised
    # test for gh issue #22338
    mpl.rcParams["legend.loc"] = value

