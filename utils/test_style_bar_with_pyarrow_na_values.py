
def test_style_bar_with_pyarrow_NA_values():
    pytest.importorskip("pyarrow")
    data = """name,age,test1,test2,teacher
        Adam,15,95.0,80,Ashby
        Bob,16,81.0,82,Ashby
        Dave,16,89.0,84,Jones
        Fred,15,,88,Jones"""
    df = read_csv(io.StringIO(data), dtype_backend="pyarrow")
    expected_substring = "style type="
    html_output = df.style.bar(subset="test1").to_html()
    assert expected_substring in html_output

