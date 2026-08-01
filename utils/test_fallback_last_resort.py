
def test_fallback_last_resort(recwarn):
    fig = plt.figure(figsize=(3, 0.5))
    fig.text(.5, .5, "Hello 🙃 World!", size=24,
             horizontalalignment='center', verticalalignment='center')
    fig.canvas.draw()
    assert all(isinstance(warn.message, UserWarning) for warn in recwarn)
    assert recwarn[0].message.args[0].startswith(
           "Glyph 128579 (\\N{UPSIDE-DOWN FACE}) missing from font(s)")

