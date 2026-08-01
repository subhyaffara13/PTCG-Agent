
def test_format_escape_latex_math(chars, expected):
    # GH 51903
    # latex-math escape works for each DataFrame cell separately. If we have
    # a combination of dollar signs and brackets, the dollar sign would apply.
    df = DataFrame([[chars]])
    s = df.style.format("{0}", escape="latex-math")
    assert s._translate(True, True)["body"][0][1]["display_value"] == expected

