from typing import Any

def grid(**interface: Any) -> str:
    if not interface["imports"]:
        return ""

    interface["statement"] += "(" + interface["imports"].pop(0)
    while interface["imports"]:
        next_import = interface["imports"].pop(0)
        next_statement = isort.comments.add_to_line(
            interface["comments"],
            interface["statement"] + ", " + next_import,
            removed=interface["remove_comments"],
            comment_prefix=interface["comment_prefix"],
        )
        if (
            len(next_statement.split(interface["line_separator"])[-1]) + 1
            > interface["line_length"]
        ):
            lines = [f"{interface['white_space']}{next_import.split(' ')[0]}"]
            for part in next_import.split(" ")[1:]:
                new_line = f"{lines[-1]} {part}"
                if len(new_line) + 1 > interface["line_length"]:
                    lines.append(f"{interface['white_space']}{part}")
                else:
                    lines[-1] = new_line
            next_import = interface["line_separator"].join(lines)
            interface["statement"] = (
                isort.comments.add_to_line(
                    interface["comments"],
                    f"{interface['statement']},",
                    removed=interface["remove_comments"],
                    comment_prefix=interface["comment_prefix"],
                )
                + f"{interface['line_separator']}{next_import}"
            )
            interface["comments"] = []
        else:
            interface["statement"] += ", " + next_import
    return f"{interface['statement']}{',' if interface['include_trailing_comma'] else ''})"


def grid(
    visible: bool | None = None,
    which: Literal["major", "minor", "both"] = "major",
    axis: Literal["both", "x", "y"] = "both",
    **kwargs,
) -> None:
    gca().grid(visible=visible, which=which, axis=axis, **kwargs)

