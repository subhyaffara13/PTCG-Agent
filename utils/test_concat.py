
def test_concat():
    assert list(concat([[], [], []])) == []
    assert (list(take(5, concat([['a', 'b'], range(1000000000)]))) ==
            ['a', 'b', 0, 1, 2])


def test_concat(styler):
    other = styler.data.agg(["mean"]).style
    styler.concat(other).set_uuid("X")
    result = styler.to_html()
    fp = "foot0_"
    expected = dedent(
        f"""\
    <tr>
      <th id="T_X_level0_row1" class="row_heading level0 row1" >b</th>
      <td id="T_X_row1_col0" class="data row1 col0" >2.690000</td>
    </tr>
    <tr>
      <th id="T_X_level0_{fp}row0" class="{fp}row_heading level0 {fp}row0" >mean</th>
      <td id="T_X_{fp}row0_col0" class="{fp}data {fp}row0 col0" >2.650000</td>
    </tr>
  </tbody>
</table>
    """
    )
    assert expected in result


def test_concat(styler):
    result = styler.concat(styler.data.agg(["sum"]).style).to_latex()
    expected = dedent(
        """\
    \\begin{tabular}{lrrl}
     & A & B & C \\\\
    0 & 0 & -0.61 & ab \\\\
    1 & 1 & -1.22 & cd \\\\
    sum & 1 & -1.830000 & abcd \\\\
    \\end{tabular}
    """
    )
    assert result == expected


def test_concat(styler):
    result = styler.concat(styler.data.agg(["sum"]).style).to_string()
    expected = dedent(
        """\
     A B C
    0 0 -0.61 ab
    1 1 -1.22 cd
    sum 1 -1.830000 abcd
    """
    )
    assert result == expected


def test_concat(styler):
    result = styler.concat(styler.data.agg(["sum"]).style).to_typst()
    expected = dedent(
        """\
    #table(
      columns: 4,
      [], [A], [B], [C],

      [0], [0], [-0.61], [ab],
      [1], [1], [-1.22], [cd],
      [sum], [1], [-1.830000], [abcd],
    )"""
    )
    assert result == expected

