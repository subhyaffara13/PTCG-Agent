
def redistribute_fw_inputs(
    global_args: Any, all_placements: Any, mesh: Any, _: int | None = None
) -> GraphArg:
    if len(global_args) != len(all_placements):
        raise AssertionError(
            f"global_args length ({len(global_args)}) != all_placements length ({len(all_placements)})"
        )
    return _redistribute(
        global_args,
        all_placements,
        mesh,
        torch.distributed.tensor._utils.compute_local_tensor_info,
    )

