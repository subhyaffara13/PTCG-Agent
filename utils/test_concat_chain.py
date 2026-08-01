
def test_concat_chain(styler):
    df = styler.data
    styler1 = styler
    styler2 = Styler(df.agg(["mean"]), precision=3)
    styler3 = Styler(df.agg(["mean"]), precision=4)
    styler1.concat(styler2).concat(styler3).set_uuid("X")
    result = styler.to_html()
    fp1 = "foot0_"
    fp2 = "foot1_"
    expected = dedent(
        f"""\
    <tr>
      <th id="T_X_level0_row1" class="row_heading level0 row1" >b</th>
      <td id="T_X_row1_col0" class="data row1 col0" >2.690000</td>
    </tr>
    <tr>
      <th id="T_X_level0_{fp1}row0" class="{fp1}row_heading level0 {fp1}row0" >mean</th>
      <td id="T_X_{fp1}row0_col0" class="{fp1}data {fp1}row0 col0" >2.650</td>
    </tr>
    <tr>
      <th id="T_X_level0_{fp2}row0" class="{fp2}row_heading level0 {fp2}row0" >mean</th>
      <td id="T_X_{fp2}row0_col0" class="{fp2}data {fp2}row0 col0" >2.6500</td>
    </tr>
  </tbody>
</table>
    """
    )
    assert expected in result


def test_concat_chain():
    # tests hidden row recursion and applied styles
    styler1 = DataFrame([[1], [9]]).style.hide([1]).highlight_min(color="red")
    styler2 = DataFrame([[9], [2]]).style.hide([0]).highlight_min(color="green")
    styler3 = DataFrame([[3], [9]]).style.hide([1]).highlight_min(color="blue")

    result = styler1.concat(styler2).concat(styler3).to_latex(convert_css=True)
    expected = dedent(
        """\
    \\begin{tabular}{lr}
     & 0 \\\\
    0 & {\\cellcolor{red}} 1 \\\\
    1 & {\\cellcolor{green}} 2 \\\\
    0 & {\\cellcolor{blue}} 3 \\\\
    \\end{tabular}
    """
    )
    assert result == expected


def test_concat_chain(styler):
    df = styler.data
    styler1 = styler
    styler2 = Styler(df.agg(["sum"]), uuid_len=0, precision=3)
    styler3 = Styler(df.agg(["sum"]), uuid_len=0, precision=4)
    result = styler1.concat(styler2).concat(styler3).to_string()
    expected = dedent(
        """\
     A B C
    0 0 -0.61 ab
    1 1 -1.22 cd
    sum 1 -1.830 abcd
    sum 1 -1.8300 abcd
    """
    )
    assert result == expected


def test_concat_chain(styler):
    df = styler.data
    styler1 = styler
    styler2 = Styler(df.agg(["sum"]), uuid_len=0, precision=3)
    styler3 = Styler(df.agg(["sum"]), uuid_len=0, precision=4)
    result = styler1.concat(styler2).concat(styler3).to_typst()
    expected = dedent(
        """\
    #table(
      columns: 4,
      [], [A], [B], [C],

      [0], [0], [-0.61], [ab],
      [1], [1], [-1.22], [cd],
      [sum], [1], [-1.830], [abcd],
      [sum], [1], [-1.8300], [abcd],
    )"""
    )
    assert result == expected

