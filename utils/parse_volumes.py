
def parse_volumes(volumes: list[str] | None) -> "list[Volume] | None":
    """Parse volume specs from CLI arguments.

    Format: hf://[TYPE/]SOURCE[/PATH]:/MOUNT_PATH[:ro|:rw]
    Where TYPE is one of: models, datasets, spaces, buckets (defaults to models if omitted).
    SOURCE is the repo/bucket identifier (e.g. 'username/my-model').
    PATH is an optional subfolder inside the repo/bucket.
    MOUNT_PATH starts with '/'.
    Optional ':ro' or ':rw' suffix for read-only or read-write.

    Examples:
        hf://my-org/my-model:/data                (model, implicit type)
        hf://models/my-org/my-model:/data         (model, explicit type)
        hf://datasets/my-org/my-dataset:/data:ro
        hf://buckets/my-org/my-bucket:/mnt
        hf://spaces/my-org/my-space:/app
        hf://datasets/org/ds/train:/data          (with path inside repo)
        hf://buckets/org/b/sub/dir:/mnt           (with path inside bucket)
    """
    if not volumes:
        return None

    result: list[Volume] = []
    for raw_spec in volumes:
        mount = parse_hf_mount(raw_spec)
        result.append(
            Volume(
                type=mount.source.type,
                source=mount.source.id,
                mount_path=mount.mount_path,
                read_only=mount.read_only,
                path=mount.source.path_in_repo or None,
                revision=mount.source.revision or None,
            )
        )
    return result

