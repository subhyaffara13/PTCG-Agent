
def test_bs4_version_fails(monkeypatch, datapath):
    bs4 = pytest.importorskip("bs4")
    pytest.importorskip("html5lib")

    monkeypatch.setattr(bs4, "__version__", "4.2")
    with pytest.raises(ImportError, match="Pandas requires version"):
        read_html(datapath("io", "data", "html", "spam.html"), flavor="bs4")

