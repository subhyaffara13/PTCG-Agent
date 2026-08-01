
def test_bar_tick_label_multiple_old_alignment():
    # Test that the alignment for class is backward compatible
    matplotlib.rcParams["ytick.alignment"] = "center"
    ax = plt.gca()
    ax.bar([1, 2.5], [1, 2], width=[0.2, 0.5], tick_label=['a', 'b'],
           align='center')

