
def _list_buckets(
    namespace: str | None,
    search: str | None,
    human_readable: bool,
    as_tree: bool,
    recursive: bool,
    token: str | None,
) -> None:
    """List buckets in a namespace."""
    # Validate incompatible flags
    if as_tree:
        raise typer.BadParameter("Cannot use --tree when listing buckets.")
    if recursive:
        raise typer.BadParameter("Cannot use --recursive when listing buckets.")

    # Handle hf://buckets/namespace format
    if namespace is not None and namespace.startswith(BUCKET_PREFIX):
        namespace = namespace[len(BUCKET_PREFIX) :]
        # Strip trailing slash if any
        namespace = namespace.rstrip("/")

    api = get_hf_api(token=token)
    items = [
        {
            "id": bucket.id,
            "private": bucket.private,
            "size": format_size(bucket.size, human_readable) if human_readable else bucket.size,
            "total_files": bucket.total_files,
            "created_at": bucket.created_at,
        }
        for bucket in api.list_buckets(namespace=namespace, search=search)
    ]
    out.table(items, alignments={"size": "right"})

