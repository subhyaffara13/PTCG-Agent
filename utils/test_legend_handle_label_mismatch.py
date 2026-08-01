
def test_legend_handle_label_mismatch():
    pl1, = plt.plot(range(10))
    pl2, = plt.plot(range(10))
    with pytest.warns(UserWarning, match="number of handles and labels"):
        legend = plt.legend(handles=[pl1, pl2], labels=["pl1", "pl2", "pl3"])
        assert len(legend.legend_handles) == 2
        assert len(legend.get_texts()) == 2

