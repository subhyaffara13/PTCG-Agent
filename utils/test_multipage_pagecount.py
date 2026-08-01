
def test_multipage_pagecount():
    with PdfPages(io.BytesIO()) as pdf:
        assert pdf.get_pagecount() == 0
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        fig.savefig(pdf, format="pdf")
        assert pdf.get_pagecount() == 1
        pdf.savefig()
        assert pdf.get_pagecount() == 2

