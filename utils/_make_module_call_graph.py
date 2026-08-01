
def _make_module_call_graph(
    in_spec: TreeSpec,
    out_spec: TreeSpec,
    module_call_signatures: dict[str, ModuleCallSignature],
    forward_arg_names: list[str] | None = None,
) -> list[ModuleCallEntry]:
    original = [
        ModuleCallEntry(fqn=fqn, signature=module_call_signatures.get(fqn))
        for fqn in _EXPORT_MODULE_HIERARCHY  # type: ignore[union-attr]
    ]
    if original[0].fqn != "":
        raise AssertionError(
            f"expected first fqn to be empty string, got {original[0].fqn!r}"
        )
    original[0].signature = ModuleCallSignature(
        inputs=[],
        outputs=[],
        in_spec=in_spec,
        out_spec=out_spec,
        forward_arg_names=forward_arg_names,
    )
    additional = [
        ModuleCallEntry(fqn=fqn, signature=signature)
        for fqn, signature in module_call_signatures.items()
        if fqn not in _EXPORT_MODULE_HIERARCHY  # type: ignore[operator]
    ]
    return [*original, *additional]

