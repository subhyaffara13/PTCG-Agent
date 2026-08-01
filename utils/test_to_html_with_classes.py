
def test_to_html_with_classes(classes, datapath):
    df = DataFrame()
    expected = expected_html(datapath, "with_classes")
    result = df.to_html(classes=classes)
    assert result == expected

