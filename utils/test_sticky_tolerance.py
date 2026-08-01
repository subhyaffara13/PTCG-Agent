
def test_sticky_tolerance():
    fig, axs = plt.subplots(2, 2)

    width = .1

    axs.flat[0].bar(x=0, height=width, bottom=20000.6)
    axs.flat[0].bar(x=1, height=width, bottom=20000.1)

    axs.flat[1].bar(x=0, height=-width, bottom=20000.6)
    axs.flat[1].bar(x=1, height=-width, bottom=20000.1)

    axs.flat[2].barh(y=0, width=-width, left=-20000.6)
    axs.flat[2].barh(y=1, width=-width, left=-20000.1)

    axs.flat[3].barh(y=0, width=width, left=-20000.6)
    axs.flat[3].barh(y=1, width=width, left=-20000.1)

