
def test_multipage_keep_empty(tmp_path):
    # An empty pdf deletes itself afterwards.
    fn = tmp_path / "a.pdf"
    with PdfPages(fn) as pdf:
        pass
    assert not fn.exists()

    # Test pdf files with content, they should never be deleted.
    fn = tmp_path / "b.pdf"
    with PdfPages(fn) as pdf:
        pdf.savefig(plt.figure())
    assert fn.exists()


def test_multipage_keep_empty(tmp_path):
    # An empty pdf deletes itself afterwards.
    fn = tmp_path / "a.pdf"
    with PdfPages(fn) as pdf:
        pass
    assert not fn.exists()

    # Test pdf files with content, they should never be deleted.
    fn = tmp_path / "b.pdf"
    with PdfPages(fn) as pdf:
        pdf.savefig(plt.figure())
    assert fn.exists()

