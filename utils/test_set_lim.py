
def test_set_lim():
    # Numpy 1.25 deprecated casting [2.] to float, catch_warnings added to error
    # with numpy 1.25 and prior to the change from gh-26597
    # can be removed once the minimum numpy version has expired the warning
    f, ax = plt.subplots()
    ax.plot(["a", "b", "c", "d"], [1, 2, 3, 4])
    with warnings.catch_warnings():
        ax.set_xlim("b", "c")

