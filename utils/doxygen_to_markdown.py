import re

def doxygen_to_markdown(string):
    """Doxygen to Markdown equations"""
    long_equations = re.sub(r"\\f\[(.*?)\\f\]", r"$$\g<1>$$", string, flags=re.DOTALL)
    inline_equations = re.sub(r"\\f\$", "$", long_equations)
    return inline_equations

