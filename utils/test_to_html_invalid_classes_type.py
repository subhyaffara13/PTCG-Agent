
def test_to_html_invalid_classes_type(classes):
    # GH 25608
    df = DataFrame()
    msg = "classes must be a string, list, or tuple"

    with pytest.raises(TypeError, match=msg):
        df.to_html(classes=classes)

