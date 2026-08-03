from typing import Any

def get_full_bucket_key(
    node: torch.fx.Node, bucket_mode: BucketMode | None
) -> tuple[str, Any]:
    """Get the full bucket key including collective type and bucket key."""
    return (get_collective_type(node), bucket_key(node, mode=bucket_mode))

