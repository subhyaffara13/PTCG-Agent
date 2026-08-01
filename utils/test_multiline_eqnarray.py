
def test_multiline_eqnarray():
    text = (
        r'\begin{eqnarray*}'
        r'foo\\'
        r'bar\\'
        r'baz\\'
        r'\end{eqnarray*}'
    )

    fig = plt.figure(figsize=(1, 1))
    fig.text(0.5, 0.5, text, usetex=True,
             horizontalalignment='center', verticalalignment='center')

