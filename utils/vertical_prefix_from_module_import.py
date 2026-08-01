
def vertical_prefix_from_module_import(**interface: Any) -> str:
    if not interface["imports"]:
        return ""

    prefix_statement = interface["statement"]
    output_statement = prefix_statement + interface["imports"].pop(0)
    comments = interface["comments"]

    statement = output_statement
    statement_with_comments = ""
    for next_import in interface["imports"]:
        statement = statement + ", " + next_import
        statement_with_comments = isort.comments.add_to_line(
            comments,
            statement,
            removed=interface["remove_comments"],
            comment_prefix=interface["comment_prefix"],
        )
        if (
            len(statement_with_comments.split(interface["line_separator"])[-1]) + 1
            > interface["line_length"]
        ):
            statement = (
                isort.comments.add_to_line(
                    comments,
                    output_statement,
                    removed=interface["remove_comments"],
                    comment_prefix=interface["comment_prefix"],
                )
                + f"{interface['line_separator']}{prefix_statement}{next_import}"
            )
            comments = []
        output_statement = statement

    if comments and statement_with_comments:
        output_statement = statement_with_comments
    return str(output_statement)

