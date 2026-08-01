
def test_non_agg_renderer(monkeypatch, recwarn):
    unpatched_init = mpl.backend_bases.RendererBase.__init__

    def __init__(self, *args, **kwargs):
        # Check that we don't instantiate any other renderer than a pdf
        # renderer to perform pdf tight layout.
        assert isinstance(self, mpl.backends.backend_pdf.RendererPdf)
        unpatched_init(self, *args, **kwargs)

    monkeypatch.setattr(mpl.backend_bases.RendererBase, "__init__", __init__)
    fig, ax = plt.subplots()
    fig.tight_layout()

