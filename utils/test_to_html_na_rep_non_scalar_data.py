
def test_to_html_na_rep_non_scalar_data(datapath):
    # GH47103
    df = DataFrame([{"a": 1, "b": [1, 2, 3]}])
    result = df.to_html(na_rep="-")
    expected = expected_html(datapath, "gh47103_expected_output")
    assert result == expected


def test_to_html_na_rep_non_scalar_data(datapath):
    # GH47103
    df = DataFrame([{"a": 1, "b": [1, 2, 3], "c": np.nan}])
    result = df.style.format(na_rep="-").to_html(table_uuid="test")
    expected = """\
<style type="text/css">
</style>
<table id="T_test">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_test_level0_col0" class="col_heading level0 col0" >a</th>
      <th id="T_test_level0_col1" class="col_heading level0 col1" >b</th>
      <th id="T_test_level0_col2" class="col_heading level0 col2" >c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_test_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_test_row0_col0" class="data row0 col0" >1</td>
      <td id="T_test_row0_col1" class="data row0 col1" >[1, 2, 3]</td>
      <td id="T_test_row0_col2" class="data row0 col2" >-</td>
    </tr>
  </tbody>
</table>
"""
    assert result == expected

