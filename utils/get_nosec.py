
def get_nosec(nosec_lines, context):
    for lineno in context["linerange"]:
        nosec = nosec_lines.get(lineno, None)
        if nosec is not None:
            return nosec
    return None

