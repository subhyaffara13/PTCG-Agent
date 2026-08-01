
def test_svg_escape():
    fig = plt.figure()
    fig.text(0.5, 0.5, "<\'\"&>", gid="<\'\"&>")
    with BytesIO() as fd:
        fig.savefig(fd, format='svg')
        buf = fd.getvalue().decode()
        assert '&lt;&apos;&quot;&amp;&gt;"' in buf

