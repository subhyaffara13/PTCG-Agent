
def build_tree(
    items: Sequence[BucketItem] | Sequence[RepoItem],
    human_readable: bool = False,
    quiet: bool = False,
) -> list[str]:
    """Build a tree representation of files and directories.

    Produces ASCII tree with size and date columns before the tree connector.
    When quiet=True, only the tree structure is shown (no size/date).
    """
    tree: dict = {}

    for item in items:
        parts = item.path.split("/")
        current = tree
        for part in parts[:-1]:
            if part not in current:
                current[part] = {"__children__": {}}
            current = current[part]["__children__"]

        final_part = parts[-1]
        if isinstance(item, BucketFolder | RepoFolder):
            if final_part not in current:
                current[final_part] = {"__children__": {}}
        else:
            current[final_part] = {"__item__": item}

    prefix_width = 0
    max_size_width = 0
    max_date_width = 0
    if not quiet:
        for item in items:
            if isinstance(item, BucketFile | RepoFile):
                size_str = format_size(item.size, human_readable)
                max_size_width = max(max_size_width, len(size_str))
                date_str = format_date(get_item_date(item), human_readable)
                max_date_width = max(max_date_width, len(date_str))
        if max_size_width > 0:
            prefix_width = max_size_width + 2 + max_date_width

    lines: list[str] = []
    _render_tree(
        tree,
        lines,
        "",
        prefix_width=prefix_width,
        max_size_width=max_size_width,
        human_readable=human_readable,
    )
    return lines

