
def test_to_html_multiindex_col_with_colspace():
    # GH#53885
    df = DataFrame([[1, 2]])
    df.columns = MultiIndex.from_tuples([(1, 1), (2, 1)])
    result = df.to_html(col_space=100)
    expected = (
        '<table border="1" class="dataframe">\n'
        "  <thead>\n"
        "    <tr>\n"
        '      <th style="min-width: 100px;"></th>\n'
        '      <th style="min-width: 100px;">1</th>\n'
        '      <th style="min-width: 100px;">2</th>\n'
        "    </tr>\n"
        "    <tr>\n"
        '      <th style="min-width: 100px;"></th>\n'
        '      <th style="min-width: 100px;">1</th>\n'
        '      <th style="min-width: 100px;">1</th>\n'
        "    </tr>\n"
        "  </thead>\n"
        "  <tbody>\n"
        "    <tr>\n"
        "      <th>0</th>\n"
        "      <td>1</td>\n"
        "      <td>2</td>\n"
        "    </tr>\n"
        "  </tbody>\n"
        "</table>"
    )
    assert result == expected

