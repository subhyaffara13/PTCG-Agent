
def test_hiding_index_columns_multiindex_trimming():
    # gh 44272
    df = DataFrame(np.arange(64).reshape(8, 8))
    df.columns = MultiIndex.from_product([[0, 1, 2, 3], [0, 1]])
    df.index = MultiIndex.from_product([[0, 1, 2, 3], [0, 1]])
    df.index.names, df.columns.names = ["a", "b"], ["c", "d"]
    styler = Styler(df, cell_ids=False, uuid_len=0)
    styler.hide([(0, 0), (0, 1), (1, 0)], axis=1).hide([(0, 0), (0, 1), (1, 0)], axis=0)
    with option_context("styler.render.max_rows", 4, "styler.render.max_columns", 4):
        result = styler.to_html()

    expected = dedent(
        """\
    <style type="text/css">
    </style>
    <table id="T_">
      <thead>
        <tr>
          <th class="blank" >&nbsp;</th>
          <th class="index_name level0" >c</th>
          <th class="col_heading level0 col3" >1</th>
          <th class="col_heading level0 col4" colspan="2">2</th>
          <th class="col_heading level0 col6" >3</th>
        </tr>
        <tr>
          <th class="blank" >&nbsp;</th>
          <th class="index_name level1" >d</th>
          <th class="col_heading level1 col3" >1</th>
          <th class="col_heading level1 col4" >0</th>
          <th class="col_heading level1 col5" >1</th>
          <th class="col_heading level1 col6" >0</th>
          <th class="col_heading level1 col_trim" >...</th>
        </tr>
        <tr>
          <th class="index_name level0" >a</th>
          <th class="index_name level1" >b</th>
          <th class="blank col3" >&nbsp;</th>
          <th class="blank col4" >&nbsp;</th>
          <th class="blank col5" >&nbsp;</th>
          <th class="blank col6" >&nbsp;</th>
          <th class="blank col7 col_trim" >&nbsp;</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th class="row_heading level0 row3" >1</th>
          <th class="row_heading level1 row3" >1</th>
          <td class="data row3 col3" >27</td>
          <td class="data row3 col4" >28</td>
          <td class="data row3 col5" >29</td>
          <td class="data row3 col6" >30</td>
          <td class="data row3 col_trim" >...</td>
        </tr>
        <tr>
          <th class="row_heading level0 row4" rowspan="2">2</th>
          <th class="row_heading level1 row4" >0</th>
          <td class="data row4 col3" >35</td>
          <td class="data row4 col4" >36</td>
          <td class="data row4 col5" >37</td>
          <td class="data row4 col6" >38</td>
          <td class="data row4 col_trim" >...</td>
        </tr>
        <tr>
          <th class="row_heading level1 row5" >1</th>
          <td class="data row5 col3" >43</td>
          <td class="data row5 col4" >44</td>
          <td class="data row5 col5" >45</td>
          <td class="data row5 col6" >46</td>
          <td class="data row5 col_trim" >...</td>
        </tr>
        <tr>
          <th class="row_heading level0 row6" >3</th>
          <th class="row_heading level1 row6" >0</th>
          <td class="data row6 col3" >51</td>
          <td class="data row6 col4" >52</td>
          <td class="data row6 col5" >53</td>
          <td class="data row6 col6" >54</td>
          <td class="data row6 col_trim" >...</td>
        </tr>
        <tr>
          <th class="row_heading level0 row_trim" >...</th>
          <th class="row_heading level1 row_trim" >...</th>
          <td class="data col3 row_trim" >...</td>
          <td class="data col4 row_trim" >...</td>
          <td class="data col5 row_trim" >...</td>
          <td class="data col6 row_trim" >...</td>
          <td class="data row_trim col_trim" >...</td>
        </tr>
      </tbody>
    </table>
    """
    )

    assert result == expected

