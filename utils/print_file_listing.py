
def print_file_listing(
    items: Sequence[BucketItem] | Sequence[RepoItem],
    *,
    human_readable: bool = False,
    as_tree: bool = False,
    recursive: bool = False,
) -> None:
    """Print a file listing in the appropriate format based on the current output mode.

    Supports tree, json, quiet, and flat human-readable views. Works with both
    BucketFile/BucketFolder and RepoFile/RepoFolder items.
    """
    if not items:
        out.text("(empty)")
        return

    has_directories = any(isinstance(item, BucketFolder | RepoFolder) for item in items)

    if as_tree:
        quiet = out.mode == OutputFormat.quiet
        for line in build_tree(items, human_readable=human_readable, quiet=quiet):
            print(line)
    elif out.mode == OutputFormat.json:
        print(json.dumps([_dataclass_to_dict(item) for item in items], indent=2))
    elif out.mode == OutputFormat.quiet:
        for item in items:
            if isinstance(item, BucketFolder | RepoFolder):
                print(f"{item.path}/")
            else:
                print(item.path)
    else:
        for item in items:
            if isinstance(item, BucketFolder | RepoFolder):
                date_str = format_date(get_item_date(item), human_readable)
                print(f"{'':>12}  {date_str:>19}  {item.path}/")
            else:
                size_str = format_size(item.size, human_readable)
                date_str = format_date(get_item_date(item), human_readable)
                print(f"{size_str:>12}  {date_str:>19}  {item.path}")

    if not recursive and has_directories:
        out.hint("Use -R to list files recursively.")

