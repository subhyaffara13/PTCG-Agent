
def prune_linear_linear(linear1: nn.Linear, linear2: nn.Linear) -> None:
    prune_linear_activation_linear(linear1, None, linear2)

