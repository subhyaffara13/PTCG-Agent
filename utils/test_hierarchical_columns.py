
def test_hierarchical_columns(parser, planet_df):
    expected = """\
<?xml version='1.0' encoding='utf-8'?>
<data>
  <row>
    <location>inner</location>
    <type>terrestrial</type>
    <count_mass>4</count_mass>
    <sum_mass>11.81</sum_mass>
    <mean_mass>2.95</mean_mass>
  </row>
  <row>
    <location>outer</location>
    <type>gas giant</type>
    <count_mass>2</count_mass>
    <sum_mass>2466.5</sum_mass>
    <mean_mass>1233.25</mean_mass>
  </row>
  <row>
    <location>outer</location>
    <type>ice giant</type>
    <count_mass>2</count_mass>
    <sum_mass>189.23</sum_mass>
    <mean_mass>94.61</mean_mass>
  </row>
  <row>
    <location>All</location>
    <type/>
    <count_mass>8</count_mass>
    <sum_mass>2667.54</sum_mass>
    <mean_mass>333.44</mean_mass>
  </row>
</data>"""

    pvt = planet_df.pivot_table(
        index=["location", "type"],
        values="mass",
        aggfunc=["count", "sum", "mean"],
        margins=True,
    ).round(2)

    output = pvt.to_xml(parser=parser)
    output = equalize_decl(output)

    assert output == expected

