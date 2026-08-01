
def test_tooltip_render(data, columns, index, styler):
    ttips = DataFrame(data=data, columns=columns, index=index)

    # GH 21266
    result = styler.set_tooltips(ttips).to_html()

    # test tooltip table level class
    assert "#T_ .pd-t {\n  visibility: hidden;\n" in result

    # test 'Min' tooltip added
    assert "#T_ #T__row0_col0:hover .pd-t {\n  visibility: visible;\n}" in result
    assert '#T_ #T__row0_col0 .pd-t::after {\n  content: "Min";\n}' in result
    assert 'class="data row0 col0" >0<span class="pd-t"></span></td>' in result

    # test 'Max' tooltip added
    assert "#T_ #T__row0_col2:hover .pd-t {\n  visibility: visible;\n}" in result
    assert '#T_ #T__row0_col2 .pd-t::after {\n  content: "Max";\n}' in result
    assert 'class="data row0 col2" >2<span class="pd-t"></span></td>' in result

    # test Nan, empty string and bad column ignored
    assert "#T_ #T__row1_col0:hover .pd-t {\n  visibility: visible;\n}" not in result
    assert "#T_ #T__row1_col1:hover .pd-t {\n  visibility: visible;\n}" not in result
    assert "#T_ #T__row0_col1:hover .pd-t {\n  visibility: visible;\n}" not in result
    assert "#T_ #T__row1_col2:hover .pd-t {\n  visibility: visible;\n}" not in result
    assert "Bad-Col" not in result

