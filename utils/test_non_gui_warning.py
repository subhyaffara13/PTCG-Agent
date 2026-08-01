
def test_non_gui_warning(monkeypatch):
    plt.subplots()

    monkeypatch.setenv("DISPLAY", ":999")

    with pytest.warns(UserWarning) as rec:
        plt.show()
        assert len(rec) == 1
        assert ('FigureCanvasPdf is non-interactive, and thus cannot be shown'
                in str(rec[0].message))

    with pytest.warns(UserWarning) as rec:
        plt.gcf().show()
        assert len(rec) == 1
        assert ('FigureCanvasPdf is non-interactive, and thus cannot be shown'
                in str(rec[0].message))

