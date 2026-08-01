
def test_scatter_empty_linestyle_pdf(ls):
    # Regression test: '', ' ', and 'none' are documented "draw nothing"
    # linestyle aliases but were not recognized by _get_dash_pattern, causing
    # savefig to PDF to crash with "zero-size array to reduction operation maximum".
    plt.switch_backend('pdf')
    fig, ax = plt.subplots()
    ax.scatter([0, 1], [0, 1], ls=ls)
    fig.savefig(io.BytesIO())

