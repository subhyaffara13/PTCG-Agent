
def test_markevery():
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.sqrt(x/10 + 0.5)

    # check marker only plot
    fig, ax = plt.subplots()
    ax.plot(x, y, 'o', label='default')
    ax.plot(x, y+1, 'd', markevery=None, label='mark all')
    ax.plot(x, y+2, 's', markevery=10, label='mark every 10')
    ax.plot(x, y+3, '+', markevery=(5, 20), label='mark every 20 starting at 5')
    ax.legend()


def test_markevery(fig_test, fig_ref, parent):
    np.random.seed(42)
    x = np.linspace(0, 1, 14)
    y = np.random.rand(len(x))

    cases_test = [None, 4, (2, 5), [1, 5, 11],
                  [0, -1], slice(5, 10, 2),
                  np.arange(len(x))[y > 0.5],
                  0.3, (0.3, 0.4)]
    cases_ref = ["11111111111111", "10001000100010", "00100001000010",
                 "01000100000100", "10000000000001", "00000101010000",
                 "01110001110110", "11011011011110", "01010011011101"]

    if parent == "figure":
        # float markevery ("relative to axes size") is not supported.
        cases_test = cases_test[:-2]
        cases_ref = cases_ref[:-2]

        def add_test(x, y, *, markevery):
            fig_test.add_artist(
                mlines.Line2D(x, y, marker="o", markevery=markevery))

        def add_ref(x, y, *, markevery):
            fig_ref.add_artist(
                mlines.Line2D(x, y, marker="o", markevery=markevery))

    elif parent == "axes":
        axs_test = iter(fig_test.subplots(3, 3).flat)
        axs_ref = iter(fig_ref.subplots(3, 3).flat)

        def add_test(x, y, *, markevery):
            next(axs_test).plot(x, y, "-gD", markevery=markevery)

        def add_ref(x, y, *, markevery):
            next(axs_ref).plot(x, y, "-gD", markevery=markevery)

    for case in cases_test:
        add_test(x, y, markevery=case)

    for case in cases_ref:
        me = np.array(list(case)).astype(int).astype(bool)
        add_ref(x, y, markevery=me)

