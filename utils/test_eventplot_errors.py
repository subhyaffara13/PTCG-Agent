
def test_eventplot_errors(err, args, kwargs, match):
    with pytest.raises(err, match=match):
        plt.eventplot(*args, **kwargs)

