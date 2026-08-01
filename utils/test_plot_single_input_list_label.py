
def test_plot_single_input_list_label():
    fig, ax = plt.subplots()
    line, = ax.plot([[0], [1]], label=['A'])
    assert line.get_label() == 'A'

