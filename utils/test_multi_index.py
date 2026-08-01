
def test_multi_index():
    s = pd.Series(
        [[0, 1, 2], np.nan, [], (3, 4)],
        name="foo",
        index=pd.MultiIndex.from_product([list("ab"), range(2)], names=["foo", "bar"]),
    )
    result = s.explode()
    index = pd.MultiIndex.from_tuples(
        [("a", 0), ("a", 0), ("a", 0), ("a", 1), ("b", 0), ("b", 1), ("b", 1)],
        names=["foo", "bar"],
    )
    expected = pd.Series(
        [0, 1, 2, np.nan, np.nan, 3, 4], index=index, dtype=object, name="foo"
    )
    tm.assert_series_equal(result, expected)


def test_multi_index(parser, planet_df):
    expected = """\
<?xml version='1.0' encoding='utf-8'?>
<data>
  <row>
    <location>inner</location>
    <type>terrestrial</type>
    <count>4</count>
    <sum>11.81</sum>
    <mean>2.95</mean>
  </row>
  <row>
    <location>outer</location>
    <type>gas giant</type>
    <count>2</count>
    <sum>2466.5</sum>
    <mean>1233.25</mean>
  </row>
  <row>
    <location>outer</location>
    <type>ice giant</type>
    <count>2</count>
    <sum>189.23</sum>
    <mean>94.61</mean>
  </row>
</data>"""

    agg = (
        planet_df.groupby(["location", "type"])["mass"]
        .agg(["count", "sum", "mean"])
        .round(2)
    )

    output = agg.to_xml(parser=parser)
    output = equalize_decl(output)

    assert output == expected

