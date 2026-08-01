
def test_figure_label():
    # pyplot figure creation, selection, and closing with label/number/instance
    plt.close('all')
    fig_today = plt.figure('today')
    plt.figure(3)
    plt.figure('tomorrow')
    plt.figure()
    plt.figure(0)
    plt.figure(1)
    plt.figure(3)
    assert plt.get_fignums() == [0, 1, 3, 4, 5]
    assert plt.get_figlabels() == ['', 'today', '', 'tomorrow', '']
    plt.close(10)
    plt.close()
    plt.close(5)
    plt.close('tomorrow')
    assert plt.get_fignums() == [0, 1]
    assert plt.get_figlabels() == ['', 'today']
    plt.figure(fig_today)
    assert plt.gcf() == fig_today

