
def boxed_nop_preserve_node_meta(
    gm: torch.fx.GraphModule, example_inputs: Sequence[InputType]
) -> Any:
    def run(args: list[Any]) -> OutputCode:
        with torch.fx.traceback.preserve_node_meta():
            return torch.fx.Interpreter(gm).boxed_run(args)

    run._boxed_call = True  # type: ignore[attr-defined]
    return run

