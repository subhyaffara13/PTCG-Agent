
def test_long_word_wrap():
    fig = plt.figure(figsize=(6, 4))
    text = fig.text(9.5, 8, 'Alonglineoftexttowrap', wrap=True)
    fig.canvas.draw()
    assert text._get_wrapped_text() == 'Alonglineoftexttowrap'

