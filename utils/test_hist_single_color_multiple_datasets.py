
def test_hist_single_color_multiple_datasets():
    data = [[0, 1, 2], [3, 4, 5]]
    _, _, bar_containers = plt.hist(data, color='k')
    for p in bar_containers[0].patches:
        assert mcolors.same_color(p.get_facecolor(), 'k')
    for p in bar_containers[1].patches:
        assert mcolors.same_color(p.get_facecolor(), 'k')

