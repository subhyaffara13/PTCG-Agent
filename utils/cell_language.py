
def cell_language(source, default_language, custom_cell_magics):
    """Return cell language and language options, if any"""
    if source:
        line = source[0]
        if default_language == "go" and _GO_DOUBLE_PERCENT_COMMAND.match(line):
            return None, None
        if default_language == "csharp":
            if line.startswith("#!"):
                lang = line[2:].strip()
                if lang in _JUPYTER_LANGUAGES:
                    source.pop(0)
                    return lang, ""
        elif line.startswith("%%"):
            magic = line[2:]
            if " " in magic:
                lang, magic_args = magic.split(" ", 1)
            else:
                lang = magic
                magic_args = ""

            if lang in _JUPYTER_LANGUAGES or lang in custom_cell_magics:
                source.pop(0)
                return lang, magic_args

    return None, None

