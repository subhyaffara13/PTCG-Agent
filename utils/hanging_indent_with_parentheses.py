from typing import Any

def hanging_indent_with_parentheses(**interface: Any) -> str:
    if not interface["imports"]:
        return ""

    line_length_limit = interface["line_length"] - 1

    interface["statement"] += "("
    next_import = interface["imports"].pop(0)
    next_statement = interface["statement"] + next_import
    # Check for first import
    if len(next_statement) > line_length_limit:
        next_statement = (
            isort.comments.add_to_line(
                interface["comments"],
                interface["statement"],
                removed=interface["remove_comments"],
                comment_prefix=interface["comment_prefix"],
            )
            + f"{interface['line_separator']}{interface['indent']}{next_import}"
        )
        interface["comments"] = []
    interface["statement"] = next_statement
    while interface["imports"]:
        next_import = interface["imports"].pop(0)
        if (
            interface["line_separator"] not in interface["statement"]
            and "#" in interface["statement"]
        ):  # pragma: no cover # TODO: fix, this is because of test run inconsistency.
            line, comments = interface["statement"].split("#", 1)
            next_statement = (
                f"{line.rstrip()}, {next_import}{interface['comment_prefix']}{comments}"
            )
        else:
            next_statement = isort.comments.add_to_line(
                interface["comments"],
                interface["statement"] + ", " + next_import,
                removed=interface["remove_comments"],
                comment_prefix=interface["comment_prefix"],
            )
        current_line = next_statement.split(interface["line_separator"])[-1]
        if len(current_line) > line_length_limit:
            next_statement = (
                isort.comments.add_to_line(
                    interface["comments"],
                    interface["statement"] + ",",
                    removed=interface["remove_comments"],
                    comment_prefix=interface["comment_prefix"],
                )
                + f"{interface['line_separator']}{interface['indent']}{next_import}"
            )
            interface["comments"] = []
        interface["statement"] = next_statement
    return f"{interface['statement']}{',' if interface['include_trailing_comma'] else ''})"

