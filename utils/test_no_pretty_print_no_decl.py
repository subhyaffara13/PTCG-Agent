
def test_no_pretty_print_no_decl(parser, geom_df):
    expected = (
        "<data><row><index>0</index><shape>square</shape>"
        "<degrees>360</degrees><sides>4.0</sides></row><row>"
        "<index>1</index><shape>circle</shape><degrees>360"
        "</degrees><sides/></row><row><index>2</index><shape>"
        "triangle</shape><degrees>180</degrees><sides>3.0</sides>"
        "</row></data>"
    )

    output = geom_df.to_xml(xml_declaration=False, pretty_print=False, parser=parser)

    # etree adds space for closed tags
    if output is not None:
        output = output.replace(" />", "/>")

    assert output == expected

