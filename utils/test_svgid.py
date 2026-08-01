
def test_svgid():
    """Test that `svg.id` rcparam appears in output svg if not None."""

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [3, 2, 1])
    fig.canvas.draw()

    # Default: svg.id = None
    with BytesIO() as fd:
        fig.savefig(fd, format='svg')
        buf = fd.getvalue().decode()

    tree = xml.etree.ElementTree.fromstring(buf)

    assert plt.rcParams['svg.id'] is None
    assert not tree.findall('.[@id]')

    # String: svg.id = str
    svg_id = 'a test for issue 28535'
    plt.rc('svg', id=svg_id)

    with BytesIO() as fd:
        fig.savefig(fd, format='svg')
        buf = fd.getvalue().decode()

    tree = xml.etree.ElementTree.fromstring(buf)

    assert plt.rcParams['svg.id'] == svg_id
    assert tree.findall(f'.[@id="{svg_id}"]')

