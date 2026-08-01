
def test_margins_errors(err, args, kwargs, match):
    with pytest.raises(err, match=match):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.margins(*args, **kwargs)


def test_margins_errors(err, args, kwargs, match):
    with pytest.raises(err, match=match):
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.margins(*args, **kwargs)

