
def test_file_handle_close(xml_books, parser):
    with open(xml_books, "rb") as f:
        read_xml(BytesIO(f.read()), parser=parser)

        assert not f.closed

