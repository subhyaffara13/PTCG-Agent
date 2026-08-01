
def test_xerr_yerr_not_none():
    ax = plt.figure().subplots()

    with pytest.raises(ValueError,
                       match="'xerr' must not contain None"):
        ax.errorbar(x=[0], y=[0], xerr=[[None], [1]], yerr=[[None], [1]])
    with pytest.raises(ValueError,
                       match="'xerr' must not contain None"):
        ax.errorbar(x=[0], y=[0], xerr=[[None], [1]])
    with pytest.raises(ValueError,
                       match="'yerr' must not contain None"):
        ax.errorbar(x=[0], y=[0], yerr=[[None], [1]])

