
def _render_tree(
    node: dict,
    lines: list[str],
    indent: str,
    prefix_width: int = 0,
    max_size_width: int = 0,
    human_readable: bool = False,
) -> None:
    """Recursively render a tree structure with size+date prefix."""
    sorted_items = sorted(node.items())
    for i, (name, value) in enumerate(sorted_items):
        is_last = i == len(sorted_items) - 1
        connector = "└── " if is_last else "├── "

        is_dir = "__children__" in value
        children = value.get("__children__", {})

        if prefix_width > 0:
            if is_dir:
                prefix = " " * prefix_width
            else:
                item = value.get("__item__")
                if item is not None:
                    size_str = format_size(item.size, human_readable)
                    date_str = format_date(get_item_date(item), human_readable)
                    prefix = f"{size_str:>{max_size_width}}  {date_str}"
                else:
                    prefix = " " * prefix_width
            lines.append(f"{prefix}  {indent}{connector}{name}{'/' if is_dir else ''}")
        else:
            lines.append(f"{indent}{connector}{name}{'/' if is_dir else ''}")

        if children:
            child_indent = indent + ("    " if is_last else "│   ")
            _render_tree(
                children,
                lines,
                child_indent,
                prefix_width=prefix_width,
                max_size_width=max_size_width,
                human_readable=human_readable,
            )

