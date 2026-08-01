
def test_text_urls():
    pikepdf = pytest.importorskip('pikepdf')

    test_url = 'https://test_text_urls.matplotlib.org/'

    fig = plt.figure(figsize=(2, 1))
    fig.text(0.1, 0.1, 'test plain 123', url=f'{test_url}plain')
    fig.text(0.1, 0.4, 'test mathtext $123$', url=f'{test_url}mathtext')

    with io.BytesIO() as fd:
        fig.savefig(fd, format='pdf')

        with pikepdf.Pdf.open(fd) as pdf:
            annots = pdf.pages[0].Annots

            # Iteration over Annots must occur within the context manager,
            # otherwise it may fail depending on the pdf structure.
            for y, fragment in [('0.1', 'plain'), ('0.4', 'mathtext')]:
                annot = next(
                    (a for a in annots if a.A.URI == f'{test_url}{fragment}'),
                    None)
                assert annot is not None
                assert getattr(annot, 'QuadPoints', None) is None
                # Positions in points (72 per inch.)
                assert annot.Rect[1] == decimal.Decimal(y) * 72


def test_text_urls():
    fig = plt.figure()

    test_url = "http://test_text_urls.matplotlib.org"
    fig.suptitle("test_text_urls", url=test_url)

    with BytesIO() as fd:
        fig.savefig(fd, format='svg')
        buf = fd.getvalue().decode()

    expected = f'<a xlink:href="{test_url}" target="_blank">'
    assert expected in buf

