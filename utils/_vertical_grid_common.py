
def _vertical_grid_common(need_trailing_char: bool, **interface: Any) -> str:
    if not interface["imports"]:
        return ""

    interface["statement"] += (
        isort.comments.add_to_line(
            interface["comments"],
            "(",
            removed=interface["remove_comments"],
            comment_prefix=interface["comment_prefix"],
        )
        + interface["line_separator"]
        + interface["indent"]
        + interface["imports"].pop(0)
    )
    while interface["imports"]:
        next_import = interface["imports"].pop(0)
        next_statement = f"{interface['statement']}, {next_import}"
        current_line_length = len(next_statement.split(interface["line_separator"])[-1])
        if interface["imports"] or interface["include_trailing_comma"]:
            # We need to account for a comma after this import.
            current_line_length += 1
        if not interface["imports"] and need_trailing_char:
            # We need to account for a closing ) we're going to add.
            current_line_length += 1
        if current_line_length > interface["line_length"]:
            next_statement = (
                f"{interface['statement']},{interface['line_separator']}"
                f"{interface['indent']}{next_import}"
            )
        interface["statement"] = next_statement
    if interface["include_trailing_comma"]:
        interface["statement"] += ","
    return str(interface["statement"])

