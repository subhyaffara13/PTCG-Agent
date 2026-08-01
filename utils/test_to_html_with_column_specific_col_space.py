
def test_to_html_with_column_specific_col_space():
    df = DataFrame(
        np.random.default_rng(2).random(size=(3, 3)), columns=["a", "b", "c"]
    )

    result = df.to_html(col_space={"a": "2em", "b": 23})
    hdrs = [x for x in result.split("\n") if re.search(r"<th[>\s]", x)]
    assert 'min-width: 2em;">a</th>' in hdrs[1]
    assert 'min-width: 23px;">b</th>' in hdrs[2]
    assert "<th>c</th>" in hdrs[3]

    result = df.to_html(col_space=["1em", 2, 3])
    hdrs = [x for x in result.split("\n") if re.search(r"<th[>\s]", x)]
    assert 'min-width: 1em;">a</th>' in hdrs[1]
    assert 'min-width: 2px;">b</th>' in hdrs[2]
    assert 'min-width: 3px;">c</th>' in hdrs[3]

