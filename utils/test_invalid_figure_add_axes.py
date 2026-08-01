
def test_invalid_figure_add_axes():
    fig = plt.figure()
    with pytest.raises(TypeError,
                       match="missing 1 required positional argument: 'rect'"):
        fig.add_axes()

    with pytest.raises(ValueError):
        fig.add_axes((.1, .1, .5, np.nan))

    with pytest.raises(TypeError, match="multiple values for argument 'rect'"):
        fig.add_axes((0, 0, 1, 1), rect=[0, 0, 1, 1])

    fig2, ax = plt.subplots()
    with pytest.raises(ValueError,
                       match="The Axes must have been created in the present "
                             "figure"):
        fig.add_axes(ax)

    fig2.delaxes(ax)
    with pytest.raises(TypeError, match=r"add_axes\(\) takes 1 positional arguments"):
        fig2.add_axes(ax, "extra positional argument")

    with pytest.raises(TypeError, match=r"add_axes\(\) takes 1 positional arguments"):
        fig.add_axes((0, 0, 1, 1), "extra positional argument")

