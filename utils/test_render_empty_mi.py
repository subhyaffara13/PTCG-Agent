
def test_render_empty_mi():
    # GH 43305
    df = DataFrame(index=MultiIndex.from_product([["A"], [0, 1]], names=[None, "one"]))
    expected = dedent(
        """\
    >
      <thead>
        <tr>
          <th class="index_name level0" >&nbsp;</th>
          <th class="index_name level1" >one</th>
        </tr>
      </thead>
    """
    )
    assert expected in df.style.to_html()

