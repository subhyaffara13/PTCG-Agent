
def test_style_charset():
    pytest.importorskip("lxml")
    xml = "<中文標籤><row><c1>1</c1><c2>2</c2></row></中文標籤>"

    xsl = """\
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
 <xsl:output omit-xml-declaration="yes" indent="yes"/>
 <xsl:strip-space elements="*"/>

 <xsl:template match="node()|@*">
     <xsl:copy>
       <xsl:apply-templates select="node()|@*"/>
     </xsl:copy>
 </xsl:template>

 <xsl:template match="中文標籤">
     <根>
       <xsl:apply-templates />
     </根>
 </xsl:template>

</xsl:stylesheet>"""

    df_orig = read_xml(StringIO(xml))
    df_style = read_xml(StringIO(xml), stylesheet=StringIO(xsl))

    tm.assert_frame_equal(df_orig, df_style)

