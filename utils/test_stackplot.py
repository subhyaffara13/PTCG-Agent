
def test_stackplot():
    fig = plt.figure()
    x = np.linspace(0, 10, 10)
    y1 = 1.0 * x
    y2 = 2.0 * x + 1
    y3 = 3.0 * x + 2
    ax = fig.add_subplot(1, 1, 1)
    ax.stackplot(x, y1, y2, y3)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 70)

    # Reuse testcase from above for a test with labeled data and with colours
    # from the Axes property cycle.
    data = {"x": x, "y1": y1, "y2": y2, "y3": y3}
    fig, ax = plt.subplots()
    ax.stackplot("x", "y1", "y2", "y3", data=data, colors=["C0", "C1", "C2"])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 70)

