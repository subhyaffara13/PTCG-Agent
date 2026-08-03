import json

def parse_json(s, **kwargs):
    """Parse a JSON string into a dict."""
    try:
        nb_dict = json.loads(s, **kwargs)
    except ValueError as e:
        message = f"Notebook does not appear to be JSON: {s!r}"
        # Limit the error message to 80 characters.  Display whatever JSON will fit.
        if len(message) > 80:
            message = message[:77] + "..."
        raise NotJSONError(message) from e
    return nb_dict

