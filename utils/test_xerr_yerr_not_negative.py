
def test_xerr_yerr_not_negative():
    ax = plt.figure().subplots()

    with pytest.raises(ValueError,
                       match="'xerr' must not contain negative values"):
        ax.errorbar(x=[0], y=[0], xerr=[[-0.5], [1]], yerr=[[-0.5], [1]])
    with pytest.raises(ValueError,
                       match="'xerr' must not contain negative values"):
        ax.errorbar(x=[0], y=[0], xerr=[[-0.5], [1]])
    with pytest.raises(ValueError,
                       match="'yerr' must not contain negative values"):
        ax.errorbar(x=[0], y=[0], yerr=[[-0.5], [1]])
    with pytest.raises(ValueError,
                       match="'yerr' must not contain negative values"):
        x = np.arange(5)
        y = [datetime.datetime(2021, 9, i * 2 + 1) for i in x]
        ax.errorbar(x=x,
                    y=y,
                    yerr=datetime.timedelta(days=-10))

