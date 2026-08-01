
def test_concat_combined():
    def html_lines(foot_prefix: str):
        assert foot_prefix.endswith("_") or foot_prefix == ""
        fp = foot_prefix
        return indent(
            dedent(
                f"""\
        <tr>
          <th id="T_X_level0_{fp}row0" class="{fp}row_heading level0 {fp}row0" >a</th>
          <td id="T_X_{fp}row0_col0" class="{fp}data {fp}row0 col0" >2.610000</td>
        </tr>
        <tr>
          <th id="T_X_level0_{fp}row1" class="{fp}row_heading level0 {fp}row1" >b</th>
          <td id="T_X_{fp}row1_col0" class="{fp}data {fp}row1 col0" >2.690000</td>
        </tr>
        """
            ),
            prefix=" " * 4,
        )

    df = DataFrame([[2.61], [2.69]], index=["a", "b"], columns=["A"])
    s1 = df.style.highlight_max(color="red")
    s2 = df.style.highlight_max(color="green")
    s3 = df.style.highlight_max(color="blue")
    s4 = df.style.highlight_max(color="yellow")

    result = s1.concat(s2).concat(s3.concat(s4)).set_uuid("X").to_html()
    expected_css = dedent(
        """\
        <style type="text/css">
        #T_X_row1_col0 {
          background-color: red;
        }
        #T_X_foot0_row1_col0 {
          background-color: green;
        }
        #T_X_foot1_row1_col0 {
          background-color: blue;
        }
        #T_X_foot1_foot0_row1_col0 {
          background-color: yellow;
        }
        </style>
        """
    )
    expected_table = (
        dedent(
            """\
            <table id="T_X">
              <thead>
                <tr>
                  <th class="blank level0" >&nbsp;</th>
                  <th id="T_X_level0_col0" class="col_heading level0 col0" >A</th>
                </tr>
              </thead>
              <tbody>
            """
        )
        + html_lines("")
        + html_lines("foot0_")
        + html_lines("foot1_")
        + html_lines("foot1_foot0_")
        + dedent(
            """\
              </tbody>
            </table>
            """
        )
    )
    assert expected_css + expected_table == result

