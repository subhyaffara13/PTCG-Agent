
def test_legend_annotate():
    fig, ax = plt.subplots()

    ax.plot([1, 2, 3], label="Line")
    ax.annotate("a", xy=(1, 1))
    ax.legend(loc=0)

    with mock.patch.object(
            fig, '_get_renderer', wraps=fig._get_renderer) as mocked_get_renderer:
        fig.savefig(io.BytesIO())

    # Finding the legend position should not require _get_renderer to be called
    mocked_get_renderer.assert_not_called()

