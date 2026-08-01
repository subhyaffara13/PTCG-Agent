
def test_draw(function, subplots, tmp_path):
    if function == nx.draw_kamada_kawai:
        pytest.importorskip("scipy", reason="draw_kamada_kawai requires scipy")
    fig, _ = subplots
    options = {"node_color": "black", "node_size": 100, "width": 3}
    function(barbell, **options)
    fig.savefig(tmp_path / "test.ps")


def test_draw(backend):
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvas
    test_backend = importlib.import_module(f'matplotlib.backends.backend_{backend}')
    TestCanvas = test_backend.FigureCanvas
    fig_test = Figure(constrained_layout=True)
    TestCanvas(fig_test)
    axes_test = fig_test.subplots(2, 2)

    # defaults to FigureCanvasBase
    fig_agg = Figure(constrained_layout=True)
    # put a backends.backend_agg.FigureCanvas on it
    FigureCanvas(fig_agg)
    axes_agg = fig_agg.subplots(2, 2)

    init_pos = [ax.get_position() for ax in axes_test.ravel()]

    fig_test.canvas.draw()
    fig_agg.canvas.draw()

    layed_out_pos_test = [ax.get_position() for ax in axes_test.ravel()]
    layed_out_pos_agg = [ax.get_position() for ax in axes_agg.ravel()]

    for init, placed in zip(init_pos, layed_out_pos_test):
        assert not np.allclose(init, placed, atol=0.005)

    for ref, test in zip(layed_out_pos_agg, layed_out_pos_test):
        np.testing.assert_allclose(ref, test, atol=0.005)

