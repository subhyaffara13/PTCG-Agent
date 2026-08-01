
def test_unicode_won():
    fig = Figure()
    fig.text(.5, .5, r'\textwon', usetex=True)

    with BytesIO() as fd:
        fig.savefig(fd, format='svg')
        buf = fd.getvalue()

    tree = xml.etree.ElementTree.fromstring(buf)
    ns = 'http://www.w3.org/2000/svg'
    won_id = 'SFSS1728-232'
    assert len(tree.findall(f'.//{{{ns}}}path[@d][@id="{won_id}"]')) == 1
    assert f'#{won_id}' in tree.find(f'.//{{{ns}}}use').attrib.values()

