
def test_latex_escape():
    assert latex_escape(r"~^\&%$#_{}") == "".join([
        r'\textasciitilde',
        r'\textasciicircum',
        r'\textbackslash',
        r'\&',
        r'\%',
        r'\$',
        r'\#',
        r'\_',
        r'\{',
        r'\}',
    ])

