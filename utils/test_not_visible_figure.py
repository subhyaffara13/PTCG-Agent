
def test_not_visible_figure():
    fig = Figure()

    buf = io.StringIO()
    fig.savefig(buf, format='svg')
    buf.seek(0)
    assert '<g ' in buf.read()

    fig.set_visible(False)
    buf = io.StringIO()
    fig.savefig(buf, format='svg')
    buf.seek(0)
    assert '<g ' not in buf.read()

