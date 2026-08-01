
def test_boxplot_legend_labels():
    # Test that legend entries are generated when passing `label`.
    np.random.seed(19680801)
    data = np.random.random((10, 4))
    fig, axs = plt.subplots(nrows=1, ncols=4)
    legend_labels = ['box A', 'box B', 'box C', 'box D']

    # Testing legend labels and patch passed to legend.
    bp1 = axs[0].boxplot(data, patch_artist=True, label=legend_labels)
    assert [v.get_label() for v in bp1['boxes']] == legend_labels
    handles, labels = axs[0].get_legend_handles_labels()
    assert labels == legend_labels
    assert all(isinstance(h, mpl.patches.PathPatch) for h in handles)

    # Testing legend without `box`.
    bp2 = axs[1].boxplot(data, label=legend_labels, showbox=False)
    # Without a box, The legend entries should be passed from the medians.
    assert [v.get_label() for v in bp2['medians']] == legend_labels
    handles, labels = axs[1].get_legend_handles_labels()
    assert labels == legend_labels
    assert all(isinstance(h, mpl.lines.Line2D) for h in handles)

    # Testing legend with number of labels different from number of boxes.
    with pytest.raises(ValueError, match='values must have same the length'):
        bp3 = axs[2].boxplot(data, label=legend_labels[:-1])

    # Test that for a string label, only the first box gets a label.
    bp4 = axs[3].boxplot(data, label='box A')
    assert bp4['medians'][0].get_label() == 'box A'
    assert all(x.get_label().startswith("_") for x in bp4['medians'][1:])

