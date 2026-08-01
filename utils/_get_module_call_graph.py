
def _get_module_call_graph(
    export_artifact: ExportArtifact,
    preserve_module_call_signature: tuple[str, ...],
    strict_mode_export: bool,
    forward_arg_names: list[str] | None = None,
) -> tuple[torch.fx.GraphModule, list[ModuleCallEntry]]:
    """
    In-place modify the graph module in export_artifact, remove _export_tracepoint nodes and
    return module_call_graph.
    """
    gm: torch.fx.GraphModule = export_artifact.aten.gm
    export_graph_signature: ExportGraphSignature = export_artifact.aten.sig
    module_call_specs: dict[str, dict[str, TreeSpec]] = (
        export_artifact.module_call_specs
    )
    in_spec: TreeSpec = export_artifact.in_spec
    out_spec: TreeSpec = export_artifact.out_spec

    # Make module signatures.
    module_call_signatures: dict[str, ModuleCallSignature] = {}
    for fqn, specs in module_call_specs.items():
        mod_fqn = _strip_root(fqn) if not strict_mode_export else fqn
        module_call_signatures[mod_fqn] = ModuleCallSignature(
            inputs=[],
            outputs=[],
            in_spec=specs["in_spec"],
            out_spec=specs["out_spec"],
            forward_arg_names=None,  # we only propagate forward_arg_names for the top level module
        )

    if len(preserve_module_call_signature) > 0:
        if not strict_mode_export:
            _rewrite_tracepoint_node(gm)
        res = CollectTracepointsPass(module_call_signatures, export_graph_signature)(gm)
        if res is None:
            raise AssertionError("CollectTracepointsPass returned None")
        gm = res.graph_module

    if _EXPORT_MODULE_HIERARCHY is None:
        raise AssertionError("_EXPORT_MODULE_HIERARCHY must not be None")
    module_call_graph = _make_module_call_graph(
        in_spec,
        out_spec,
        module_call_signatures,
        forward_arg_names,
    )
    return gm, module_call_graph

