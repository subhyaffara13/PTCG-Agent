
def test_pdf_type1_font_subsetting():
    """Test that fonts in PDF output are properly subset."""
    pikepdf = pytest.importorskip("pikepdf")

    mpl.rcParams["text.usetex"] = True
    mpl.rcParams["text.latex.preamble"] = r"\usepackage{amssymb}"
    fig, ax = plt.subplots()
    ax.text(0.2, 0.7, r"$\int_{-\infty}^{\aleph}\sqrt{\alpha\beta\gamma}\mathrm{d}x$")
    ax.text(0.2, 0.5, r"$\mathfrak{x}\circledcirc\mathfrak{y}\in\mathbb{R}$")

    with TemporaryFile() as tmpfile:
        fig.savefig(tmpfile, format="pdf")
        tmpfile.seek(0)
        pdf = pikepdf.Pdf.open(tmpfile)

        length = {}
        page = pdf.pages[0]
        for font_name, font in page.Resources.Font.items():
            assert font.Subtype == "/Type1", (
                f"Font {font_name}={font} is not a Type 1 font"
            )

            # Subsetted font names have a 6-character tag followed by a '+'
            base_font = str(font["/BaseFont"]).removeprefix("/")
            assert re.match(r"^[A-Z]{6}\+", base_font), (
                f"Font {font_name}={base_font} lacks a subset indicator tag"
            )
            assert "/FontFile" in font.FontDescriptor, (
                f"Type 1 font {font_name}={base_font} is not embedded"
            )
            _, original_name = base_font.split("+", 1)
            length[original_name] = len(bytes(font["/FontDescriptor"]["/FontFile"]))

    print("Embedded font stream lengths:", length)
    # We should have several fonts, each much smaller than the original.
    # I get under 10kB on my system for each font, but allow 15kB in case
    # of differences in the font files.
    assert {
        'CMEX10',
        'CMMI12',
        'CMR12',
        'CMSY10',
        'CMSY8',
        'EUFM10',
        'MSAM10',
        'MSBM10',
    }.issubset(length), "Missing expected fonts in the PDF"
    for font_name, length in length.items():
        assert length < 15_000, (
            f"Font {font_name}={length} is larger than expected"
        )

