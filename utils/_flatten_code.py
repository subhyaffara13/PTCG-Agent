
def _flatten_code(code):
    "Flattens the code from a list of tuples."
    flat_code = []
    for c in code:
        flat_code.extend(c)

    return flat_code

