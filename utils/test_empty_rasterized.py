
def test_empty_rasterized():
    # Check that empty figures that are rasterised save to pdf files fine
    fig, ax = plt.subplots()
    ax.plot([], [], rasterized=True)
    fig.savefig(io.BytesIO(), format="pdf")

