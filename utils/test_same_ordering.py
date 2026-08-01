
def test_same_ordering(datapath):
    pytest.importorskip("bs4")
    pytest.importorskip("lxml")
    pytest.importorskip("html5lib")

    filename = datapath("io", "data", "html", "valid_markup.html")
    dfs_lxml = read_html(filename, index_col=0, flavor=["lxml"])
    dfs_bs4 = read_html(filename, index_col=0, flavor=["bs4"])
    assert_framelist_equal(dfs_lxml, dfs_bs4)

