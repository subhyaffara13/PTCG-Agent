from typing import Any

def hanging_indent(**interface: Any) -> str:
    if not interface["imports"]:
        return ""

    line_length_limit = interface["line_length"] - 3

    next_import = interface["imports"].pop(0)
    next_statement = interface["statement"] + next_import
    # Check for first import
    if len(next_statement) > line_length_limit:
        next_statement = (
            _hanging_indent_end_line(interface["statement"])
            + interface["line_separator"]
            + interface["indent"]
            + next_import
        )

    interface["statement"] = next_statement
    while interface["imports"]:
        next_import = interface["imports"].pop(0)
        next_statement = interface["statement"] + ", " + next_import
        if len(next_statement.split(interface["line_separator"])[-1]) > line_length_limit:
            next_statement = (
                _hanging_indent_end_line(interface["statement"] + ",")
                + f"{interface['line_separator']}{interface['indent']}{next_import}"
            )
        interface["statement"] = next_statement

    if interface["comments"]:
        statement_with_comments = isort.comments.add_to_line(
            interface["comments"],
            interface["statement"],
            removed=interface["remove_comments"],
            comment_prefix=interface["comment_prefix"],
        )
        if len(statement_with_comments.split(interface["line_separator"])[-1]) <= (
            line_length_limit + 2
        ):
            return statement_with_comments
        return (
            _hanging_indent_end_line(interface["statement"])
            + str(interface["line_separator"])
            + isort.comments.add_to_line(
                interface["comments"],
                interface["indent"],
                removed=interface["remove_comments"],
                comment_prefix=interface["comment_prefix"].lstrip(),
            )
        )
    return str(interface["statement"])

