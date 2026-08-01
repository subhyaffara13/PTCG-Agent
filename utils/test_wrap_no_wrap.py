
def test_wrap_no_wrap():
    fig = plt.figure(figsize=(6, 4))
    text = fig.text(0, 0, 'non wrapped text', wrap=True)
    fig.canvas.draw()
    assert text._get_wrapped_text() == 'non wrapped text'

