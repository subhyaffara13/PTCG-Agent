
def _prepare_exported_program_for_export(
    exported_program: torch.export.ExportedProgram,
    *,
    registry: _registration.ONNXRegistry,
) -> torch.export.ExportedProgram:
    """Decompose and apply pre-export transformations to the exported program."""

    with (
        # Support the dynamism with 0/1 input dim
        torch.fx.experimental._config.patch(backed_size_oblivious=True),  # type: ignore[attr-defined]
    ):
        # Decompose the graph given the implemented torch ops in ONNX
        exported_program = _fx_passes.decompose_with_registry(
            exported_program, registry
        )

        graph_module = exported_program.graph_module
        # Include explicit type promotion nodes
        _fx_passes.insert_type_promotion_nodes(graph_module)
        graph_module = _fx_passes.remove_assertion_nodes(graph_module)
        # Reassign the graph module to save some runtime.
        exported_program._graph_module = graph_module
        return exported_program

