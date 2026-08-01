
def parse_cluster_shards(resp, **options):
    """
    Parse CLUSTER SHARDS response.
    """
    if isinstance(resp[0], dict):
        return resp
    shards = []
    for x in resp:
        shard = {"slots": [], "nodes": []}
        for i in range(0, len(x[1]), 2):
            shard["slots"].append((x[1][i], (x[1][i + 1])))
        nodes = x[3]
        for node in nodes:
            dict_node = {}
            for i in range(0, len(node), 2):
                dict_node[node[i]] = node[i + 1]
            shard["nodes"].append(dict_node)
        shards.append(shard)

    return shards

