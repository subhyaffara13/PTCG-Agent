
def test_set_current_figure_via_subfigure():
    fig1 = plt.figure()
    subfigs = fig1.subfigures(2)

    plt.figure()
    assert plt.gcf() != fig1

    current = plt.figure(subfigs[1])
    assert plt.gcf() == fig1
    assert current == fig1

