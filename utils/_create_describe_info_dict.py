
def _create_describe_info_dict(G):
    info = {}
    if G.name != "":
        info["Name of Graph"] = G.name
    info.update(
        {
            "Number of nodes": len(G),
            "Number of edges": G.number_of_edges(),
            "Directed": G.is_directed(),
            "Multigraph": G.is_multigraph(),
            "Tree": nx.is_tree(G),
            "Bipartite": nx.is_bipartite(G),
        }
    )
    if len(G) == 0:
        return info

    degree_values = dict(nx.degree(G)).values()
    avg_degree = sum(degree_values) / len(G)
    max_degree, min_degree = max(degree_values), min(degree_values)
    info["Average degree (min, max)"] = f"{avg_degree:.2f} ({min_degree}, {max_degree})"

    if G.is_directed():
        info["Number of strongly connected components"] = (
            nx.number_strongly_connected_components(G)
        )
        info["Number of weakly connected components"] = (
            nx.number_weakly_connected_components(G)
        )
    else:
        info["Number of connected components"] = nx.number_connected_components(G)
    return info

