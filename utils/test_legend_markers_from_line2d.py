
def test_legend_markers_from_line2d():
    # Test that markers can be copied for legend lines (#17960)
    _markers = ['.', '*', 'v']
    fig, ax = plt.subplots()
    lines = [mlines.Line2D([0], [0], ls='None', marker=mark)
             for mark in _markers]
    labels = ["foo", "bar", "xyzzy"]
    markers = [line.get_marker() for line in lines]
    legend = ax.legend(lines, labels)

    new_markers = [line.get_marker() for line in legend.get_lines()]
    new_labels = [text.get_text() for text in legend.get_texts()]

    assert markers == new_markers == _markers
    assert labels == new_labels

