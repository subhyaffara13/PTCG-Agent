
def _export_forward_backward(
    ep: torch.export.ExportedProgram, joint_loss_index: int = 0
) -> torch.export.ExportedProgram:
    """
    WARNING: This API is highly unstable and will be subject to change in the future.
    """
    from torch._decomp import core_aten_decompositions

    ep = _decompose_exported_program(
        ep,
        cia_to_decomp={},
        python_decomp_table=core_aten_decompositions(),
        joint_loss_index=joint_loss_index,
        # For serialization purpose, we don't want to decompose custom triton ops.
        # If users would like to decompose custom triton ops, they could do it
        # with run_decompositions() API.
        decompose_custom_triton_ops=False,
    )
    gm, new_graph_signature = _copy_graph_module_and_signature(ep)
    _remove_detach_pass(gm, new_graph_signature)

    return ep._update(gm, new_graph_signature)

