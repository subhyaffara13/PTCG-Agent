
def _repr_tree_defs(data: _ImportTree, indent_str: str | None = None) -> str:
    """Return a string which represents imports as a tree."""
    lines = []
    nodes_items = data.items()
    for i, (mod, (sub, files)) in enumerate(sorted(nodes_items, key=lambda x: x[0])):
        files_list = "" if not files else f"({','.join(sorted(files))})"
        if indent_str is None:
            lines.append(f"{mod} {files_list}")
            sub_indent_str = "  "
        else:
            lines.append(rf"{indent_str}\-{mod} {files_list}")
            if i == len(nodes_items) - 1:
                sub_indent_str = f"{indent_str}  "
            else:
                sub_indent_str = f"{indent_str}| "
        if sub and isinstance(sub, dict):
            lines.append(_repr_tree_defs(sub, sub_indent_str))
    return "\n".join(lines)

