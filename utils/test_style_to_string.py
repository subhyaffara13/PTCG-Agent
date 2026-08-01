
def test_style_to_string(geom_df):
    pytest.importorskip("lxml")
    xsl = """\
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text" indent="yes" />
    <xsl:strip-space elements="*"/>

    <xsl:param name="delim"><xsl:text>               </xsl:text></xsl:param>
    <xsl:template match="/data">
        <xsl:text>      shape  degrees  sides&#xa;</xsl:text>
        <xsl:apply-templates select="row"/>
    </xsl:template>

    <xsl:template match="row">
        <xsl:value-of select="concat(index, ' ',
                                     substring($delim, 1, string-length('triangle')
                                               - string-length(shape) + 1),
                                     shape,
                                     substring($delim, 1, string-length(name(degrees))
                                               - string-length(degrees) + 2),
                                     degrees,
                                     substring($delim, 1, string-length(name(sides))
                                               - string-length(sides) + 2),
                                     sides)"/>
         <xsl:text>&#xa;</xsl:text>
    </xsl:template>
</xsl:stylesheet>"""

    out_str = geom_df.to_string()
    out_xml = geom_df.to_xml(na_rep="NaN", stylesheet=StringIO(xsl))

    assert out_xml == out_str

