
def test_load_case_sensitive(monkeypatch):
    mpl_test_backend = SimpleNamespace(**vars(backend_template))
    mock_show = MagicMock()
    monkeypatch.setattr(
        mpl_test_backend.FigureManagerTemplate, "pyplot_show", mock_show)
    monkeypatch.setitem(sys.modules, "mpl_Test_Backend", mpl_test_backend)
    mpl.use("module://mpl_Test_Backend")
    plt.show()
    mock_show.assert_called_with()

