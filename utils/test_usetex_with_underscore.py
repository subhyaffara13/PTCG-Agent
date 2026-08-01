
def test_usetex_with_underscore():
    plt.rcParams["text.usetex"] = True
    df = {"a_b": range(5)[::-1], "c": range(5)}
    fig, ax = plt.subplots()
    ax.plot("c", "a_b", data=df)
    ax.legend()
    ax.text(0, 0, "foo_bar", usetex=True)
    plt.draw()

