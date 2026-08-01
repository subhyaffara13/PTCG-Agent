
def test_literal_xml_raises():
    # GH 53809
    pytest.importorskip("lxml")
    msg = "|".join([r".*No such file or directory", r".*Invalid argument"])

    with pytest.raises((FileNotFoundError, OSError), match=msg):
        read_xml(xml_default_nmsp)

