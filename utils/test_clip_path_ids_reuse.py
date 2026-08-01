
def test_clip_path_ids_reuse():
    fig, circle = Figure(), Circle((0, 0), radius=10)
    for i in range(5):
        ax = fig.add_subplot()
        aimg = ax.imshow([[i]])
        aimg.set_clip_path(circle)

    inner_circle = Circle((0, 0), radius=1)
    ax = fig.add_subplot()
    aimg = ax.imshow([[0]])
    aimg.set_clip_path(inner_circle)

    with BytesIO() as fd:
        fig.savefig(fd, format='svg')
        buf = fd.getvalue()

    tree = xml.etree.ElementTree.fromstring(buf)
    ns = 'http://www.w3.org/2000/svg'

    clip_path_ids = set()
    for node in tree.findall(f'.//{{{ns}}}clipPath[@id]'):
        node_id = node.attrib['id']
        assert node_id not in clip_path_ids  # assert ID uniqueness
        clip_path_ids.add(node_id)
    assert len(clip_path_ids) == 2  # only two clipPaths despite reuse in multiple axes

