
def test_mathwrap():
    fig = plt.figure(figsize=(5, 4))
    s = r'This is a very $\overline{\mathrm{long}}$ line of Mathtext.'
    text = fig.text(0, 0.5, s, size=40, wrap=True)
    fig.canvas.draw()
    assert text._get_wrapped_text() == ('This is a very $\\overline{\\mathrm{long}}$\n'
                                        'line of Mathtext.')

