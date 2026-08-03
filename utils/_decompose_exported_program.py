from typing import Callable

def _decompose_exported_program(
    ep,
    *,
    cia_to_decomp: dict[torch._ops.OperatorBase, Callable],
    python_decomp_table: dict[torch._ops.OperatorBase, Callable],
    joint_loss_index: int | None,
    decompose_custom_triton_ops: bool,
):
    (
        gm,
        new_graph_signature,
        state_dict,
    ) = _decompose_and_get_gm_with_new_signature_constants(
        ep,
        cia_to_decomp=cia_to_decomp,
        python_decomp_table=python_decomp_table,
        joint_loss_index=joint_loss_index,
        decompose_custom_triton_ops=decompose_custom_triton_ops,
    )

    # The signatures of ep.module_call_graph refer to input / output nodes of
    # the original graph module. However, the new graph module may have
    # new nodes due to decompositions. So we need to update these signatures
    # in the decomposed exported program's module_call_graph.
    new_module_call_graph = _get_updated_module_call_graph(
        ep.graph_module,
        ep.graph_signature,
        gm,
        new_graph_signature,
        ep.module_call_graph,
    )

    # TODO unfortunately preserving graph-level metadata is not
    # working well with aot_export. So we manually copy it.
    # (The node-level meta is addressed above.)
    gm.meta.update(ep.graph_module.meta)

    new_range_constraints = _get_updated_range_constraints(
        gm,
        ep.range_constraints,
    )

    exported_program = ExportedProgram(
        root=gm,
        graph=gm.graph,
        graph_signature=new_graph_signature,
        state_dict=state_dict,
        range_constraints=new_range_constraints,
        module_call_graph=new_module_call_graph,
        example_inputs=ep.example_inputs,
        constants=ep.constants,
    )
    return exported_program

