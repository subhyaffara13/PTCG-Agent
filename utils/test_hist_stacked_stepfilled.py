
def test_hist_stacked_stepfilled():
    # make some data
    d1 = np.linspace(1, 3, 20)
    d2 = np.linspace(0, 10, 50)
    fig, ax = plt.subplots()
    ax.hist((d1, d2), histtype="stepfilled", stacked=True)

    # Reuse testcase from above for a labeled data test
    data = {"x": (d1, d2)}
    fig, ax = plt.subplots()
    ax.hist("x", histtype="stepfilled", stacked=True, data=data)

