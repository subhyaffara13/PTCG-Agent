
def test_zorder_and_explicit_rasterization():
    fig, ax = plt.subplots()
    ax.set_rasterization_zorder(5)
    ln, = ax.plot(range(5), rasterized=True, zorder=1)
    with io.BytesIO() as b:
        fig.savefig(b, format='pdf')

