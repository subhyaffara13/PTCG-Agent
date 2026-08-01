
def repro_get_args(
    options: Any, mod: nn.Module, load_args: Any
) -> tuple[torch.fx.GraphModule, list[Any]]:
    mod, args = repro_common(options, mod, load_args)
    return mod, args


def repro_get_args(
    options: Any,
    exported_program: ExportedProgram,
    config_patches: dict[str, Any] | None,
) -> tuple[torch.fx.GraphModule, Any, Any]:
    mod, args, kwargs = repro_common(options, exported_program)
    return mod, args, kwargs

