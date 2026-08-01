
def test_multipage_properfinalize():
    pdfio = io.BytesIO()
    with PdfPages(pdfio) as pdf:
        for i in range(10):
            fig, ax = plt.subplots()
            ax.set_title('This is a long title')
            fig.savefig(pdf, format="pdf")
    s = pdfio.getvalue()
    assert s.count(b'startxref') == 1
    assert len(s) < 40000

