
def _metadata_hash(code: str, node_metadata: dict) -> str:
    """
    Create a content-addressed hash from code and metadata.

    Args:
        code: The source code string
        lineno_map: Mapping from line numbers to node indices
        node_metadata: Metadata for each node

    Returns:
        A 51-character base32-encoded hash
    """
    import json

    # Create a deterministic string representation of all components
    # We use JSON to ensure consistent serialization
    hash_data = {
        "code": code,
        "node_metadata": node_metadata,
    }
    hashing_str = json.dumps(hash_data).encode("utf-8")

    # [:51] to strip off the "Q====" suffix common to every hash value.
    return (
        base64.b32encode(hashlib.sha256(hashing_str).digest())[:51]
        .decode("utf-8")
        .lower()
    )

