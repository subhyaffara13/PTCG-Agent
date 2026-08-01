
def test_to_html_encoding(float_frame, temp_file):
    # GH 28663
    float_frame.to_html(temp_file, encoding="gbk")
    expected = temp_file.read_text(encoding="gbk")
    assert float_frame.to_html() == expected

