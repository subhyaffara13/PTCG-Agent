
def test_pdfpages_fspath(tmp_path):
    with PdfPages(tmp_path / 'unused.pdf') as pdf:
        pdf.savefig(plt.figure())

