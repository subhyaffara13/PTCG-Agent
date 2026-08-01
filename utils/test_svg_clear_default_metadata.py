
def test_svg_clear_default_metadata(monkeypatch):
    # Makes sure that setting a default metadata to `None`
    # removes the corresponding tag from the metadata.
    monkeypatch.setenv('SOURCE_DATE_EPOCH', '19680801')

    metadata_contains = {'creator': mpl.__version__, 'date': '1970-08-16',
                         'format': 'image/svg+xml', 'type': 'StillImage'}

    SVGNS = '{http://www.w3.org/2000/svg}'
    RDFNS = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
    CCNS = '{http://creativecommons.org/ns#}'
    DCNS = '{http://purl.org/dc/elements/1.1/}'

    fig, ax = plt.subplots()
    for name in metadata_contains:
        with BytesIO() as fd:
            fig.savefig(fd, format='svg', metadata={name.title(): None})
            buf = fd.getvalue().decode()

        root = xml.etree.ElementTree.fromstring(buf)
        work, = root.findall(f'./{SVGNS}metadata/{RDFNS}RDF/{CCNS}Work')
        for key in metadata_contains:
            data = work.findall(f'./{DCNS}{key}')
            if key == name:
                # The one we cleared is not there
                assert not data
                continue
            # Everything else should be there
            data, = data
            xmlstr = xml.etree.ElementTree.tostring(data, encoding="unicode")
            assert metadata_contains[key] in xmlstr

