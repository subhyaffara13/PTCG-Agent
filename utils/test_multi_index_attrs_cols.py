
def test_multi_index_attrs_cols(parser, planet_df):
    expected = """\
<?xml version='1.0' encoding='utf-8'?>
<data>
  <row location="inner" type="terrestrial" count="4" \
sum="11.81" mean="2.95"/>
  <row location="outer" type="gas giant" count="2" \
sum="2466.5" mean="1233.25"/>
  <row location="outer" type="ice giant" count="2" \
sum="189.23" mean="94.61"/>
</data>"""

    agg = (
        planet_df.groupby(["location", "type"])["mass"]
        .agg(["count", "sum", "mean"])
        .round(2)
    )
    output = agg.to_xml(attr_cols=list(agg.reset_index().columns.values), parser=parser)
    output = equalize_decl(output)

    assert output == expected

