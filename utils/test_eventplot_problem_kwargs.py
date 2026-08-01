
def test_eventplot_problem_kwargs(recwarn):
    """
    test that 'singular' versions of LineCollection props raise an
    MatplotlibDeprecationWarning rather than overriding the 'plural' versions
    (e.g., to prevent 'color' from overriding 'colors', see issue #4297)
    """
    np.random.seed(0)

    data1 = np.random.random([20]).tolist()
    data2 = np.random.random([10]).tolist()
    data = [data1, data2]

    fig = plt.figure()
    axobj = fig.add_subplot()

    axobj.eventplot(data,
                    colors=['r', 'b'],
                    color=['c', 'm'],
                    linewidths=[2, 1],
                    linewidth=[1, 2],
                    linestyles=['solid', 'dashed'],
                    linestyle=['dashdot', 'dotted'])

    assert len(recwarn) == 3
    assert all(issubclass(wi.category, mpl.MatplotlibDeprecationWarning)
               for wi in recwarn)

