
def lower_exported_program(
    exported_program: ExportedProgram, model_name: str, backend_id: str
) -> tuple[ExportedProgram, AOTI_FILES]:
    """
    Lower an exported program to AOTInductor and return a delegate ExportedProgram
    with the `executorch_call_delegate` HOP
    """
    args, kwargs = exported_program.example_inputs
    out_spec = exported_program.call_spec.out_spec
    flat_ep = get_new_ep_with_flat_inputs_outputs(exported_program)
    flat_inputs, _ = pytree.tree_flatten((args, kwargs))

    aoti_files = torch._inductor.aot_compile(
        flat_ep.module(), tuple(flat_inputs), options={"aot_inductor.package": True}
    )
    if not isinstance(aoti_files, list):
        raise AssertionError(
            f"aoti_files must be a list, got {type(aoti_files).__name__}"
        )

    lowered_aoti_module = LoweredBackendModule(
        flat_ep, backend_id, module_name=model_name
    )

    def patched_forward(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        flat_inputs, _ = pytree.tree_flatten((args, kwargs))
        flat_outputs = torch._higher_order_ops.executorch_call_delegate(
            self, *flat_inputs
        )
        if out_spec is not None and flat_outputs is not None:
            return pytree.tree_unflatten(flat_outputs, out_spec)
        else:
            return flat_outputs

    lowered_aoti_module.forward = types.MethodType(patched_forward, lowered_aoti_module)  # type: ignore[method-assign]

    aoti_delegate_ep = torch.export.export(lowered_aoti_module, args, kwargs)

    return aoti_delegate_ep, aoti_files

