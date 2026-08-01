
def test_plot_multiple_label_incorrect_length_exception():
    # check that exception is raised if multiple labels
    # are given, but number of on labels != number of lines
    with pytest.raises(ValueError):
        x = [1, 2, 3]
        y = [[1, 2],
             [2, 5],
             [4, 9]]
        label = ['high', 'low', 'medium']
        fig, ax = plt.subplots()
        ax.plot(x, y, label=label)

