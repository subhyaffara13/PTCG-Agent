
def test_to_html_invalid_justify(justify):
    # GH 17527
    df = DataFrame()
    msg = "Invalid value for justify parameter"

    with pytest.raises(ValueError, match=msg):
        df.to_html(justify=justify)

