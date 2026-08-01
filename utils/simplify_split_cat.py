
def simplify_split_cat(match: Match, split_sections: list[int], dim: int):
    if not isinstance(split_sections, (list, tuple)):  # Unnormalized split
        return
    split_node = next(node for node in match.nodes if node.target is torch.split)

    SplitCatSimplifier().simplify(match.graph, split_node, split_sections)

