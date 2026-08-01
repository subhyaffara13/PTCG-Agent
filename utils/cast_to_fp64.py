
def cast_to_fp64(
    model: torch.fx.GraphModule, inputs: list[Any]
) -> tuple[torch.fx.GraphModule, list[Any]]:
    return cast_to(torch.float64, model, inputs)

