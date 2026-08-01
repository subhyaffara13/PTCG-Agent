
def _args(n: torch.fx.Node) -> list[torch.fx.node.Argument]:
    args: list[torch.fx.node.Argument] = []
    torch.fx.map_arg((n.args, n.kwargs), args.append)
    return args

