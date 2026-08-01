
def test_style_to_csv(geom_df):
    pytest.importorskip("lxml")
    xsl = """\
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text" indent="yes" />
    <xsl:strip-space elements="*"/>

    <xsl:param name="delim">,</xsl:param>
    <xsl:template match="/data">
        <xsl:text>,shape,degrees,sides&#xa;</xsl:text>
        <xsl:apply-templates select="row"/>
    </xsl:template>

    <xsl:template match="row">
        <xsl:value-of select="concat(index, $delim, shape, $delim,
                                     degrees, $delim, sides)"/>
         <xsl:text>&#xa;</xsl:text>
    </xsl:template>
</xsl:stylesheet>"""

    out_csv = geom_df.to_csv(lineterminator="\n")

    if out_csv is not None:
        out_csv = out_csv.strip()
    out_xml = geom_df.to_xml(stylesheet=StringIO(xsl))

    assert out_csv == out_xml

