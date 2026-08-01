
def test_set_fig_size():
    fig = plt.figure()

    # check figwidth
    fig.set_figwidth(5)
    assert fig.get_figwidth() == 5

    # check figheight
    fig.set_figheight(1)
    assert fig.get_figheight() == 1

    # check using set_size_inches
    fig.set_size_inches(2, 4)
    assert fig.get_figwidth() == 2
    assert fig.get_figheight() == 4

    # check using tuple to first argument
    fig.set_size_inches((1, 3))
    assert fig.get_figwidth() == 1
    assert fig.get_figheight() == 3

