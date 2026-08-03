import re

def quote_docstring(docstr: str) -> str:
    """Returns docstring correctly encapsulated in a single or double quoted form."""
    # Uses repr to get hint on the correct quotes and escape everything properly.
    # Creating multiline string for prettier output.
    docstr_repr = "\n".join(re.split(r"(?<=[^\\])\\n", repr(docstr)))

    if docstr_repr.startswith("'"):
        # Enforce double quotes when it's safe to do so.
        # That is when double quotes are not in the string
        # or when it doesn't end with a single quote.
        if '"' not in docstr_repr[1:-1] and docstr_repr[-2] != "'":
            return f'"""{docstr_repr[1:-1]}"""'
        return f"''{docstr_repr}''"
    else:
        return f'""{docstr_repr}""'

