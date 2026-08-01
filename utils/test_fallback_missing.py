
def test_fallback_missing(recwarn, font_list):
    fig = plt.figure()
    fig.text(.5, .5, "Hello 🙃 World!", family=font_list)
    fig.canvas.draw()
    assert all(isinstance(warn.message, UserWarning) for warn in recwarn)
    # not sure order is guaranteed on the font listing so
    assert recwarn[0].message.args[0].startswith(
           "Glyph 128579 (\\N{UPSIDE-DOWN FACE}) missing from font(s)")
    assert all([font in recwarn[0].message.args[0] for font in font_list])

