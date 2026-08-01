
def add_dont_constant_fold(op: torch.fx.node.Target) -> None:
    global _dont_constant_fold
    _dont_constant_fold.append(op)

