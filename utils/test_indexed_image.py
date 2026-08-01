
def test_indexed_image():
    # An image with low color count should compress to a palette-indexed format.
    pikepdf = pytest.importorskip('pikepdf')

    data = np.zeros((256, 1, 3), dtype=np.uint8)
    data[:, 0, 0] = np.arange(256)  # Maximum unique colours for an indexed image.

    rcParams['pdf.compression'] = True
    fig = plt.figure()
    fig.figimage(data, resize=True)
    buf = io.BytesIO()
    fig.savefig(buf, format='pdf', dpi='figure')

    with pikepdf.Pdf.open(buf) as pdf:
        page, = pdf.pages
        image, = page.images.values()
        pdf_image = pikepdf.PdfImage(image)
        assert pdf_image.indexed
        pil_image = pdf_image.as_pil_image()
        rgb = np.asarray(pil_image.convert('RGB'))

    np.testing.assert_array_equal(data, rgb)

