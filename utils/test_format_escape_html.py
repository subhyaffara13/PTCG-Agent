
def test_format_escape_html(escape, exp):
    chars = '<>&"%$#_{}~^\\~ ^ \\ '
    df = DataFrame([[chars]])

    s = Styler(df, uuid_len=0).format("&{0}&", escape=None)
    expected = f'<td id="T__row0_col0" class="data row0 col0" >&{chars}&</td>'
    assert expected in s.to_html()

    # only the value should be escaped before passing to the formatter
    s = Styler(df, uuid_len=0).format("&{0}&", escape=escape)
    expected = f'<td id="T__row0_col0" class="data row0 col0" >&{exp}&</td>'
    assert expected in s.to_html()

    # also test format_index()
    styler = Styler(DataFrame(columns=[chars]), uuid_len=0)
    styler.format_index("&{0}&", escape=None, axis=1)
    assert styler._translate(True, True)["head"][0][1]["display_value"] == f"&{chars}&"
    styler.format_index("&{0}&", escape=escape, axis=1)
    assert styler._translate(True, True)["head"][0][1]["display_value"] == f"&{exp}&"

