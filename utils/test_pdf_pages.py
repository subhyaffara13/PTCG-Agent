import os

def test_pdf_pages(system):
    rc_pdflatex = {
        'font.family': 'serif',
        'pgf.rcfonts': False,
        'pgf.texsystem': system,
    }
    mpl.rcParams.update(rc_pdflatex)

    fig1, ax1 = plt.subplots()
    ax1.plot(range(5))
    fig1.tight_layout()

    fig2, ax2 = plt.subplots(figsize=(3, 2))
    ax2.plot(range(5))
    fig2.tight_layout()

    path = os.path.join(result_dir, f'pdfpages_{system}.pdf')
    md = {
        'Author': 'me',
        'Title': 'Multipage PDF with pgf',
        'Subject': 'Test page',
        'Keywords': 'test,pdf,multipage',
        'ModDate': datetime.datetime(
            1968, 8, 1, tzinfo=datetime.timezone(datetime.timedelta(0))),
        'Trapped': 'Unknown'
    }

    with PdfPages(path, metadata=md) as pdf:
        pdf.savefig(fig1)
        pdf.savefig(fig2)
        pdf.savefig(fig1)

        assert pdf.get_pagecount() == 3

