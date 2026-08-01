
def _generate_inputs_for_submodules(
    model: torch.nn.Module,
    target_submodules: Iterable[str],
    args: tuple[Any, ...],
    kwargs: dict[str, Any] | None = None,
) -> dict[str, tuple[Any, Any]]:
    """
    Generate inputs for targeting submdoules in the given model. Note that if two submodules refer to the same obj, this
    function doesn't work.

    Args:
        model: root model.
        inputs: inputs to the root model.
        target_submodules: submodules that we want to generate inputs for.

    Returns:
        A dict that maps from submodule name to its inputs.
    """
    kwargs = kwargs or {}

    handles = []
    results = {}
    submodule_to_names = {mod: name for name, mod in model.named_modules()}

    def pre_forward(module, module_args, module_kwargs):
        results[submodule_to_names[module]] = (module_args, module_kwargs)

    try:
        for name, mod in model.named_modules():
            if name in target_submodules:
                handles.append(
                    mod.register_forward_pre_hook(pre_forward, with_kwargs=True)
                )
        model(*args, **kwargs)
    except Exception as e:
        warnings.warn(
            f"Failed to generate submodule inputs because of the following error:\n{e}",
            stacklevel=2,
        )
    finally:
        for h in handles:
            h.remove()
    return results

