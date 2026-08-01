
def relax_json_loads(text, catch=False):
    """Parse a JSON string or similar"""
    text = text.strip()
    try:
        return loads(text)
    except JSONDecodeError:
        pass

    if not catch:
        return ast.literal_eval(text)

    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        pass

    return incorrectly_encoded_metadata(text)

