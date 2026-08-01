
def test_tex_special_chars(tmp_path):
    fig = plt.figure()
    fig.text(.5, .5, "%_^ $a_b^c$")
    buf = BytesIO()
    fig.savefig(buf, format="png", backend="pgf")
    buf.seek(0)
    t = plt.imread(buf)
    assert not (t == 1).all()  # The leading "%" didn't eat up everything.

