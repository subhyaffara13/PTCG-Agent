
def get_new_ep_with_flat_inputs_outputs(ep: ExportedProgram) -> ExportedProgram:
    class FlattenedModule(torch.nn.Module):
        def __init__(
            self,
            original_module: torch.fx.GraphModule,
            in_spec: pytree.TreeSpec,
            out_spec: pytree.TreeSpec,
        ) -> None:
            super().__init__()
            self.original_module = original_module
            self.in_spec = in_spec
            self.out_spec = out_spec

        def forward(self, *flat_inputs):  # type: ignore[no-untyped-def]
            # Unflatten inputs to original structure
            inputs = pytree.tree_unflatten(flat_inputs, self.in_spec)
            args, kwargs = inputs
            outputs = self.original_module(*args, **kwargs)
            # Flatten outputs
            flat_outputs, _ = pytree.tree_flatten(outputs)
            return tuple(flat_outputs)

    flattened_module = FlattenedModule(
        ep.module(), ep.call_spec.in_spec, ep.call_spec.out_spec
    )
    args, kwargs = ep.example_inputs
    flat_inputs, _ = pytree.tree_flatten((args, kwargs))
    flat_ep = torch.export.export(flattened_module, tuple(flat_inputs))

    return flat_ep

