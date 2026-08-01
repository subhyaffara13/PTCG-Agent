
def test_multiline():
    plt.figure()
    ax = plt.subplot(1, 1, 1)
    ax.set_title("multiline\ntext alignment")

    plt.text(
        0.2, 0.5, "TpTpTp\n$M$\nTpTpTp", size=20, ha="center", va="top")

    plt.text(
        0.5, 0.5, "TpTpTp\n$M^{M^{M^{M}}}$\nTpTpTp", size=20,
        ha="center", va="top")

    plt.text(
        0.8, 0.5, "TpTpTp\n$M_{q_{q_{q}}}$\nTpTpTp", size=20,
        ha="center", va="top")

    plt.xlim(0, 1)
    plt.ylim(0, 0.8)

    ax.set_xticks([])
    ax.set_yticks([])

