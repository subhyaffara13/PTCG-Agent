
def test_cc_to_xml():
    assert (
        tools.dict_to_xml({'filename': CC_TO_XML_CASE})
        == '''<ccm>
              <metric>
                <complexity>6</complexity>
                <unit>name</unit>
                <classification>B</classification>
                <file>filename</file>
                <startLineNumber>12</startLineNumber>
                <endLineNumber>16</endLineNumber>
              </metric>
              <metric>
                <complexity>8</complexity>
                <unit>Classname</unit>
                <classification>B</classification>
                <file>filename</file>
                <startLineNumber>17</startLineNumber>
                <endLineNumber>29</endLineNumber>
              </metric>
              <metric>
                <complexity>7</complexity>
                <unit>Classname.name</unit>
                <classification>B</classification>
                <file>filename</file>
                <startLineNumber>19</startLineNumber>
                <endLineNumber>26</endLineNumber>
              </metric>
              <metric>
                <complexity>4</complexity>
                <unit>aux</unit>
                <classification>A</classification>
                <file>filename</file>
                <startLineNumber>13</startLineNumber>
                <endLineNumber>17</endLineNumber>
              </metric>
              <metric>
                <complexity>10</complexity>
                <unit>name</unit>
                <classification>B</classification>
                <file>filename</file>
                <startLineNumber>12</startLineNumber>
                <endLineNumber>16</endLineNumber>
              </metric>
            </ccm>'''.replace(
            '\n', ''
        ).replace(
            ' ', ''
        )
    )

