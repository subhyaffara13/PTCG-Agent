
def parse_cluster_shards_unified(resp, **options):
    """
    Parse CLUSTER SHARDS into the approved unified shape.

    Top-level shard keys and nested node attribute keys are strings for both
    RESP2 and RESP3 wire responses.
    """
    if not resp:
        return resp
    if isinstance(resp[0], dict):
        shards = []
        for shard_resp in resp:
            slots = shard_resp.get(b"slots", shard_resp.get("slots", []))
            nodes = shard_resp.get(b"nodes", shard_resp.get("nodes", []))
            shard = {
                "slots": slots,
                "nodes": [
                    {str_if_bytes(k): v for k, v in node.items()}
                    if isinstance(node, dict)
                    else node
                    for node in nodes
                ],
            }
            shards.append(shard)
        return shards

    shards = []
    for x in resp:
        shard = {"slots": [], "nodes": []}
        for i in range(0, len(x[1]), 2):
            shard["slots"].append((x[1][i], x[1][i + 1]))
        nodes = x[3]
        for node in nodes:
            dict_node = {}
            for i in range(0, len(node), 2):
                dict_node[str_if_bytes(node[i])] = node[i + 1]
            shard["nodes"].append(dict_node)
        shards.append(shard)
    return shards

