
def parse_cluster_shards_with_str_keys(resp, **options):
    """
    Parse CLUSTER SHARDS with string top-level structural keys.

    RESP2 parsing exposes top-level shard keys as ``"slots"``/``"nodes"``
    while node attribute keys keep the connection's decoded/raw form. RESP3 can
    return top-level shard dictionaries directly, so normalize only the
    structural shard keys and preserve nested node dictionaries as delivered.
    """
    if not resp:
        return resp
    if not isinstance(resp[0], dict):
        return parse_cluster_shards(resp, **options)

    shards = []
    for shard_resp in resp:
        slots = shard_resp.get(b"slots", shard_resp.get("slots", []))
        nodes = shard_resp.get(b"nodes", shard_resp.get("nodes", []))
        shard = {
            "slots": [
                tuple(slot) if isinstance(slot, list) else slot for slot in slots
            ],
            "nodes": [dict(node) if isinstance(node, dict) else node for node in nodes],
        }
        shards.append(shard)
    return shards

