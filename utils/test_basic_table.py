
def test_basic_table(styler):
    result = styler.to_typst()
    expected = dedent(
        """\
    #table(
      columns: 4,
      [], [A], [B], [C],

      [0], [0], [-0.61], [ab],
      [1], [1], [-1.22], [cd],
    )"""
    )
    assert result == expected

