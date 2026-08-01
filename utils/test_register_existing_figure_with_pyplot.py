
def test_register_existing_figure_with_pyplot():
    from matplotlib.figure import Figure
    # start with a standalone figure
    fig = Figure()
    assert fig.canvas.manager is None
    with pytest.raises(AttributeError):
        # Heads-up: This will change to returning None in the future
        # See docstring for the Figure.number property
        fig.number
    # register the Figure with pyplot
    plt.figure(fig)
    assert fig.number == 1
    # the figure can now be used in pyplot
    plt.suptitle("my title")
    assert fig.get_suptitle() == "my title"
    # it also has a manager that is properly wired up in the pyplot state
    assert plt._pylab_helpers.Gcf.get_fig_manager(fig.number) is fig.canvas.manager
    # and we can regularly switch the pyplot state
    fig2 = plt.figure()
    assert fig2.number == 2
    assert plt.figure(1) is fig
    assert plt.gcf() is fig

