
def test_incorrect_xsl_syntax(geom_df):
    lxml_etree = pytest.importorskip("lxml.etree")

    xsl = """\
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" encoding="utf-8" indent="yes" >
    <xsl:strip-space elements="*"/>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="row/*">
        <field>
            <xsl:attribute name="field">
                <xsl:value-of select="name()"/>
            </xsl:attribute>
            <xsl:value-of select="text()"/>
        </field>
    </xsl:template>
</xsl:stylesheet>"""

    with pytest.raises(
        lxml_etree.XMLSyntaxError, match="Opening and ending tag mismatch"
    ):
        geom_df.to_xml(stylesheet=StringIO(xsl))


def test_incorrect_xsl_syntax(kml_cta_rail_lines):
    lxml_etree = pytest.importorskip("lxml.etree")

    xsl = """\
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                              xmlns:k="http://www.opengis.net/kml/2.2"/>
    <xsl:output method="xml" omit-xml-declaration="yes"
                cdata-section-elements="k:description" indent="yes"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="node()|@*">
     <xsl:copy>
       <xsl:apply-templates select="node()|@*"/>
     </xsl:copy>
    </xsl:template>

    <xsl:template match="k:MultiGeometry|k:LineString">
        <xsl:apply-templates select='*'/>
    </xsl:template>

    <xsl:template match="k:description|k:Snippet|k:Style"/>
</xsl:stylesheet>"""

    with pytest.raises(
        lxml_etree.XMLSyntaxError, match="Extra content at the end of the document"
    ):
        read_xml(kml_cta_rail_lines, stylesheet=StringIO(xsl))

