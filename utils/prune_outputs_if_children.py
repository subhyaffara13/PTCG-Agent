
def prune_outputs_if_children(node):
    # if there are children, remove this node's "outputs"
    # so we only see outputs at the leaf level
    if node.get("children"):
        node.pop("outputs", None)
        for child in node["children"]:
            prune_outputs_if_children(child)

