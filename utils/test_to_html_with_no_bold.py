
def test_to_html_with_no_bold():
    df = DataFrame({"x": np.random.default_rng(2).standard_normal(5)})
    html = df.to_html(bold_rows=False)
    result = html[html.find("</thead>")]
    assert "<strong" not in result

