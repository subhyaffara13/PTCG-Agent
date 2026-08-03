from typing import Any

def vertical(**interface: Any) -> str:
    if not interface["imports"]:
        return ""

    first_import = (
        isort.comments.add_to_line(
            interface["comments"],
            interface["imports"].pop(0) + ",",
            removed=interface["remove_comments"],
            comment_prefix=interface["comment_prefix"],
        )
        + interface["line_separator"]
        + interface["white_space"]
    )

    _imports = ("," + interface["line_separator"] + interface["white_space"]).join(
        interface["imports"]
    )
    _comma_maybe = "," if interface["include_trailing_comma"] else ""
    return f"{interface['statement']}({first_import}{_imports}{_comma_maybe})"

