
def _make_explanation(a, b):
    """Explanation for a failed assert -- the a and b arguments are List[str]"""
    return ["--- actual / +++ expected"] + [
        line.strip("\n") for line in difflib.ndiff(a, b)
    ]

