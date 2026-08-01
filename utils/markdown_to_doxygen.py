
def markdown_to_doxygen(string):
    """Markdown to Doxygen equations"""
    long_equations = re.sub(r"(?<!\\)\$\$(.*?)(?<!\\)\$\$", r"\\f[\g<1>\\f]", string, flags=re.DOTALL)
    inline_equations = re.sub(r"(?<!(\\|\$))\$(?!\$)", r"\\f$", long_equations)
    return inline_equations

