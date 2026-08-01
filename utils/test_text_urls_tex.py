
def test_text_urls_tex():
    pikepdf = pytest.importorskip('pikepdf')

    test_url = 'https://test_text_urls.matplotlib.org/'

    fig = plt.figure(figsize=(2, 1))
    fig.text(0.1, 0.7, 'test tex $123$', usetex=True, url=f'{test_url}tex')

    with io.BytesIO() as fd:
        fig.savefig(fd, format='pdf')

        with pikepdf.Pdf.open(fd) as pdf:
            annots = pdf.pages[0].Annots

            # Iteration over Annots must occur within the context manager,
            # otherwise it may fail depending on the pdf structure.
            annot = next(
                (a for a in annots if a.A.URI == f'{test_url}tex'),
                None)
            assert annot is not None
            # Positions in points (72 per inch.)
            assert annot.Rect[1] == decimal.Decimal('0.7') * 72

