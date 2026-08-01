
def test_stylesheet_with_etree(geom_df):
    xsl = """\
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" encoding="utf-8" indent="yes" />
    <xsl:strip-space elements="*"/>

    <xsl:template match="@*|node(*)">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>"""

    with pytest.raises(ValueError, match="To use stylesheet, you need lxml installed"):
        geom_df.to_xml(parser="etree", stylesheet=StringIO(xsl))


def test_stylesheet_with_etree(kml_cta_rail_lines, xsl_flatten_doc):
    pytest.importorskip("lxml")
    with pytest.raises(
        ValueError, match=("To use stylesheet, you need lxml installed")
    ):
        read_xml(kml_cta_rail_lines, parser="etree", stylesheet=xsl_flatten_doc)

