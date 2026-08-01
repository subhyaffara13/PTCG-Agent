
def _split_code_at_show(text, function_name):
    """Split code at plt.show()."""

    is_doctest = contains_doctest(text)
    if function_name is None:
        parts = []
        part = []
        for line in text.split("\n"):
            if ((not is_doctest and line.startswith('plt.show(')) or
                   (is_doctest and line.strip() == '>>> plt.show()')):
                part.append(line)
                parts.append("\n".join(part))
                part = []
            else:
                part.append(line)
        if "\n".join(part).strip():
            parts.append("\n".join(part))
    else:
        parts = [text]
    return is_doctest, parts

