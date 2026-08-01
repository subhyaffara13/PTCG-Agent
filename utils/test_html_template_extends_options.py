
def test_html_template_extends_options(datapath):
    # make sure if templates are edited tests are updated as are setup fixtures
    # to understand the dependency
    path = datapath("..", "io", "formats", "templates", "html.tpl")
    with open(path, encoding="utf-8") as file:
        result = file.read()
    assert "{% include html_style_tpl %}" in result
    assert "{% include html_table_tpl %}" in result

