
def test_legend_handle_label_mismatch_no_len():
    pl1, = plt.plot(range(10))
    pl2, = plt.plot(range(10))
    legend = plt.legend(handles=iter([pl1, pl2]),
                        labels=iter(["pl1", "pl2", "pl3"]))
    assert len(legend.legend_handles) == 2
    assert len(legend.get_texts()) == 2

