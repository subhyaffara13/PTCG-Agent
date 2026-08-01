
def test_hiding_index_columns_multiindex_alignment():
    # gh 43644
    midx = MultiIndex.from_product(
        [["i0", "j0"], ["i1"], ["i2", "j2"]], names=["i-0", "i-1", "i-2"]
    )
    cidx = MultiIndex.from_product(
        [["c0"], ["c1", "d1"], ["c2", "d2"]], names=["c-0", "c-1", "c-2"]
    )
    df = DataFrame(np.arange(16).reshape(4, 4), index=midx, columns=cidx)
    styler = Styler(df, uuid_len=0)
    styler.hide(level=1, axis=0).hide(level=0, axis=1)
    styler.hide([("j0", "i1", "j2")], axis=0)
    styler.hide([("c0", "d1", "d2")], axis=1)
    result = styler.to_html()
    expected = dedent(
        """\
    <style type="text/css">
    </style>
    <table id="T_">
      <thead>
        <tr>
          <th class="blank" >&nbsp;</th>
          <th class="index_name level1" >c-1</th>
          <th id="T__level1_col0" class="col_heading level1 col0" colspan="2">c1</th>
          <th id="T__level1_col2" class="col_heading level1 col2" >d1</th>
        </tr>
        <tr>
          <th class="blank" >&nbsp;</th>
          <th class="index_name level2" >c-2</th>
          <th id="T__level2_col0" class="col_heading level2 col0" >c2</th>
          <th id="T__level2_col1" class="col_heading level2 col1" >d2</th>
          <th id="T__level2_col2" class="col_heading level2 col2" >c2</th>
        </tr>
        <tr>
          <th class="index_name level0" >i-0</th>
          <th class="index_name level2" >i-2</th>
          <th class="blank col0" >&nbsp;</th>
          <th class="blank col1" >&nbsp;</th>
          <th class="blank col2" >&nbsp;</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th id="T__level0_row0" class="row_heading level0 row0" rowspan="2">i0</th>
          <th id="T__level2_row0" class="row_heading level2 row0" >i2</th>
          <td id="T__row0_col0" class="data row0 col0" >0</td>
          <td id="T__row0_col1" class="data row0 col1" >1</td>
          <td id="T__row0_col2" class="data row0 col2" >2</td>
        </tr>
        <tr>
          <th id="T__level2_row1" class="row_heading level2 row1" >j2</th>
          <td id="T__row1_col0" class="data row1 col0" >4</td>
          <td id="T__row1_col1" class="data row1 col1" >5</td>
          <td id="T__row1_col2" class="data row1 col2" >6</td>
        </tr>
        <tr>
          <th id="T__level0_row2" class="row_heading level0 row2" >j0</th>
          <th id="T__level2_row2" class="row_heading level2 row2" >i2</th>
          <td id="T__row2_col0" class="data row2 col0" >8</td>
          <td id="T__row2_col1" class="data row2 col1" >9</td>
          <td id="T__row2_col2" class="data row2 col2" >10</td>
        </tr>
      </tbody>
    </table>
    """
    )
    assert result == expected

