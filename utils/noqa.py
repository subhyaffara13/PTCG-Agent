from typing import Any

def noqa(**interface: Any) -> str:
    _imports = ", ".join(interface["imports"])
    retval = f"{interface['statement']}{_imports}"
    comment_str = " ".join(interface["comments"])
    if interface["comments"]:
        if (
            len(retval) + len(interface["comment_prefix"]) + 1 + len(comment_str)
            <= interface["line_length"]
        ):
            return f"{retval}{interface['comment_prefix']} {comment_str}"
        if "NOQA" in interface["comments"]:
            return f"{retval}{interface['comment_prefix']} {comment_str}"
        return f"{retval}{interface['comment_prefix']} NOQA {comment_str}"

    if len(retval) <= interface["line_length"]:
        return retval
    return f"{retval}{interface['comment_prefix']} NOQA"

