
def _get_range_constraints(
    mod: torch.nn.Module,
    export_artifact: ExportArtifact,
    args,
    kwargs,
    dynamic_shapes,
):
    gm: torch.fx.GraphModule = export_artifact.aten.gm
    export_graph_signature: ExportGraphSignature = export_artifact.aten.sig
    fake_mode: FakeTensorMode = export_artifact.fake_mode
    num_lifted = next(
        (
            i
            for i, s in enumerate(export_graph_signature.input_specs)
            if s.kind == InputKind.USER_INPUT
        ),
        len(export_graph_signature.input_specs),
    )
    combined_args = _combine_args(mod, args, kwargs)

    # This is because we trace based on the kwargs passed in from user
    # not based on the signature. I feel it would be better to just enforce
    # one ordering at the start of tracing to avoid confusions, but that is
    # bigger refactor, so do this to unblock for now.
    combined_args_traced_order = {}
    for arg in combined_args:
        if arg not in kwargs:
            combined_args_traced_order[arg] = combined_args[arg]

    for key in kwargs:
        combined_args_traced_order[key] = kwargs[key]

    combined_args = combined_args_traced_order

    range_constraints = make_constraints(
        fake_mode,
        gm,
        combined_args,
        dynamic_shapes,
        num_lifted,
    )
    return range_constraints

