
def test_replaced_css_class_names():
    css = {
        "row_heading": "ROWHEAD",
        # "col_heading": "COLHEAD",
        "index_name": "IDXNAME",
        # "col": "COL",
        "row": "ROW",
        # "col_trim": "COLTRIM",
        "row_trim": "ROWTRIM",
        "level": "LEVEL",
        "data": "DATA",
        "blank": "BLANK",
    }
    midx = MultiIndex.from_product([["a", "b"], ["c", "d"]])
    styler_mi = Styler(
        DataFrame(np.arange(16).reshape(4, 4), index=midx, columns=midx),
        uuid_len=0,
    ).set_table_styles(css_class_names=css)
    styler_mi.index.names = ["n1", "n2"]
    styler_mi.hide(styler_mi.index[1:], axis=0)
    styler_mi.hide(styler_mi.columns[1:], axis=1)
    styler_mi.map_index(lambda v: "color: red;", axis=0)
    styler_mi.map_index(lambda v: "color: green;", axis=1)
    styler_mi.map(lambda v: "color: blue;")
    expected = dedent(
        """\
    <style type="text/css">
    #T__ROW0_col0 {
      color: blue;
    }
    #T__LEVEL0_ROW0, #T__LEVEL1_ROW0 {
      color: red;
    }
    #T__LEVEL0_col0, #T__LEVEL1_col0 {
      color: green;
    }
    </style>
    <table id="T_">
      <thead>
        <tr>
          <th class="BLANK" >&nbsp;</th>
          <th class="IDXNAME LEVEL0" >n1</th>
          <th id="T__LEVEL0_col0" class="col_heading LEVEL0 col0" >a</th>
        </tr>
        <tr>
          <th class="BLANK" >&nbsp;</th>
          <th class="IDXNAME LEVEL1" >n2</th>
          <th id="T__LEVEL1_col0" class="col_heading LEVEL1 col0" >c</th>
        </tr>
        <tr>
          <th class="IDXNAME LEVEL0" >n1</th>
          <th class="IDXNAME LEVEL1" >n2</th>
          <th class="BLANK col0" >&nbsp;</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th id="T__LEVEL0_ROW0" class="ROWHEAD LEVEL0 ROW0" >a</th>
          <th id="T__LEVEL1_ROW0" class="ROWHEAD LEVEL1 ROW0" >c</th>
          <td id="T__ROW0_col0" class="DATA ROW0 col0" >0</td>
        </tr>
      </tbody>
    </table>
    """
    )
    result = styler_mi.to_html()
    assert result == expected

