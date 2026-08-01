
def test_axis_errors(err, args, kwargs, match):
    with pytest.raises(err, match=match):
        plt.axis(*args, **kwargs)

