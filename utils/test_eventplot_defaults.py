
def test_eventplot_defaults():
    """
    test that eventplot produces the correct output given the default params
    (see bug #3728)
    """
    np.random.seed(0)

    data1 = np.random.random([32, 20]).tolist()
    data2 = np.random.random([6, 20]).tolist()
    data = data1 + data2

    fig = plt.figure()
    axobj = fig.add_subplot()
    axobj.eventplot(data)

