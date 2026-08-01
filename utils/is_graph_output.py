
def is_graph_output(node: torch.fx.Node) -> bool:
    return all(user.op == "output" for user in node.users)

