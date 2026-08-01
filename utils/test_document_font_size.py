
def test_document_font_size():
    mpl.rcParams.update({
        'pgf.texsystem': 'xelatex',
        'pgf.rcfonts': False,
        'pgf.preamble': r'\usepackage{unicode-math}',
    })
    plt.figure()
    plt.plot([],
             label=r'$this is a very very very long math label a \times b + 10^{-3}$ '
                   r'and some text'
             )
    plt.plot([],
             label=r'\normalsize the document font size is \the\fontdimen6\font'
             )
    plt.legend()

