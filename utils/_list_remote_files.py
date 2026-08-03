from typing import Any

def _list_remote_files(api: "HfApi", bucket_id: str, prefix: str) -> Iterator[tuple[str, int, float, Any]]:
    """List all files in a bucket with a given prefix.

    Yields:
        tuple: (relative_path, size, mtime_ms, bucket_file) for each file.
            bucket_file is the BucketFile object from list_bucket_tree.
    """
    for item in api.list_bucket_tree(bucket_id, prefix=prefix or None, recursive=True):
        if isinstance(item, BucketFolder):
            continue
        path = item.path
        # Remove prefix from path to get relative path
        # Only strip prefix if it's followed by "/" (directory boundary) or is exact match
        if prefix:
            if path.startswith(prefix + "/"):
                rel_path = path[len(prefix) + 1 :]
            elif path == prefix:
                # Exact match: the file IS the prefix (e.g., single file download)
                rel_path = path.rsplit("/", 1)[-1] if "/" in path else path
            else:
                # Path doesn't match prefix pattern (e.g., "submarine.txt" for prefix "sub")
                # Skip this file - it was returned by the API but doesn't belong to this prefix
                continue
        else:
            rel_path = path
        mtime_ms = item.mtime.timestamp() * 1000 if item.mtime else 0
        yield rel_path, item.size, mtime_ms, item

