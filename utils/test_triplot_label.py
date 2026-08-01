
def test_triplot_label():
    x = [0, 2, 1]
    y = [0, 0, 1]
    data = [[0, 1, 2]]
    fig, ax = plt.subplots()
    lines, markers = ax.triplot(x, y, data, label='label')
    handles, labels = ax.get_legend_handles_labels()
    assert labels == ['label']
    assert len(handles) == 1
    assert handles[0] is lines

