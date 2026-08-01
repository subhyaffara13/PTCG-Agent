
def test_cull_markers():
    x = np.random.random(20000)
    y = np.random.random(20000)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'k.')
    ax.set_xlim(2, 3)

    pdf = io.BytesIO()
    fig.savefig(pdf, format="pdf")
    assert len(pdf.getvalue()) < 8000

    svg = io.BytesIO()
    fig.savefig(svg, format="svg")
    assert len(svg.getvalue()) < 20000

