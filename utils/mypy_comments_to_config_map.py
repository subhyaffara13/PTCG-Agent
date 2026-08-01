
def mypy_comments_to_config_map(line: str, template: Options) -> tuple[dict[str, str], list[str]]:
    """Rewrite the mypy comment syntax into ini file syntax."""
    options = {}
    entries, errors = split_directive(line)
    for entry in entries:
        if "=" not in entry:
            name = entry
            value = None
        else:
            name, value = (x.strip() for x in entry.split("=", 1))

        name = name.replace("-", "_")
        if value is None:
            value = "True"
        options[name] = value

    return options, errors

