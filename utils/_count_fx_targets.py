
def _count_fx_targets(
    exported_program: torch.export.ExportedProgram,
) -> defaultdict[str, int]:
    """Count the number of targets for each node in the exported program."""
    fx_node_target_count: defaultdict[str, int] = defaultdict(int)
    for node in exported_program.graph.nodes:
        if node.op == "call_function":
            fx_node_target_count[str(node.target)] += 1
    return fx_node_target_count

