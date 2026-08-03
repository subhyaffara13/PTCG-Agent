from typing import Tuple

def _next_term(text: str, openmetrics: bool) -> Tuple[str, str, str]:
    """Extract the next comma-separated label term from the text. The results
    are stripped terms for the label name, label value, and then the remainder
    of the string including the final , or }.
    
    Raises ValueError if the term is empty and we're in openmetrics mode.
    """
    
    # There may be a leading comma, which is fine here.
    if text[0] == ',':
        text = text[1:]
        if not text:
            return "", "", ""
        if text[0] == ',':
            raise ValueError("multiple commas")

    splitpos = _next_unquoted_char(text, '=,}')
    if splitpos >= 0 and text[splitpos] == "=":
        labelname = text[:splitpos]
        text = text[splitpos + 1:]
        splitpos = _next_unquoted_char(text, ',}')
    else:
        labelname = "__name__"

    if splitpos == -1:
        splitpos = len(text)
    term = text[:splitpos]
    if not term and openmetrics:
        raise ValueError("empty term:", term)
    
    rest = text[splitpos:]
    return labelname, term.strip(), rest.strip()

