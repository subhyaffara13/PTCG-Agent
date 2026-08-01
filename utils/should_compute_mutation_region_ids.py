
def should_compute_mutation_region_ids(graph: torch.fx.Graph) -> bool:
    return "mutation_region_id" not in next(iter(graph.nodes)).meta

