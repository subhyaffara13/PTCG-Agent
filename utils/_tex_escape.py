
def _tex_escape(text):
    r"""
    Do some necessary and/or useful substitutions for texts to be included in
    LaTeX documents.
    """
    return text.replace("\N{MINUS SIGN}", r"\ensuremath{-}")

