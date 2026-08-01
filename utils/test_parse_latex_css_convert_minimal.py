
def test_parse_latex_css_convert_minimal(styler, env, inner_env, convert, exp):
    # parameters ensure longtable template is also tested
    styler.highlight_max(props="font-weight:bold;")
    result = styler.to_latex(convert_css=convert, environment=env)
    expected = dedent(
        f"""\
        0 & 0 & \\{exp} -0.61 & ab \\\\
        1 & \\{exp} 1 & -1.22 & \\{exp} cd \\\\
        \\end{{{inner_env}}}
    """
    )
    assert expected in result

