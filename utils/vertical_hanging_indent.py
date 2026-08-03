from typing import Any

def vertical_hanging_indent(**interface: Any) -> str:
    _line_with_comments = isort.comments.add_to_line(
        interface["comments"],
        "",
        removed=interface["remove_comments"],
        comment_prefix=interface["comment_prefix"],
    )
    _imports = ("," + interface["line_separator"] + interface["indent"]).join(interface["imports"])
    _comma_maybe = "," if interface["include_trailing_comma"] else ""
    return (
        f"{interface['statement']}({_line_with_comments}{interface['line_separator']}"
        f"{interface['indent']}{_imports}{_comma_maybe}{interface['line_separator']})"
    )

