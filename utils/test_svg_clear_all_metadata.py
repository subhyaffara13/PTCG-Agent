
def test_svg_clear_all_metadata():
    # Makes sure that setting all default metadata to `None`
    # removes the metadata tag from the output.

    fig, ax = plt.subplots()
    with BytesIO() as fd:
        fig.savefig(fd, format='svg', metadata={'Date': None, 'Creator': None,
                                                'Format': None, 'Type': None})
        buf = fd.getvalue().decode()

    SVGNS = '{http://www.w3.org/2000/svg}'

    root = xml.etree.ElementTree.fromstring(buf)
    assert not root.findall(f'./{SVGNS}metadata')

