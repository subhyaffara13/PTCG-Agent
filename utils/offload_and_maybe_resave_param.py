
def offload_and_maybe_resave_param(
    target_name: str,
    param: torch.Tensor,
    loading_info: LoadStateDictInfo,
    disk_offload_folder: str,
    disk_offload_index: dict,
    applied_ops: WeightConverter | WeightRenaming,
) -> dict:
    """Takes care of correctly offloading `param`. If it's not already present in the `disk_offload_index`, or if any
    WeightConverter operations have been applied, it will resave the new parameter. Otherwise, it will use the original
    `disk_offload_index` for this given param."""
    # We need to remove from missing keys
    loading_info.missing_keys.discard(target_name)
    # If not already offloaded, or if we applied any special Operation except Renaming, we need to re-save
    if target_name not in disk_offload_index or isinstance(applied_ops, WeightConverter):
        disk_offload_index = offload_weight(param, target_name, disk_offload_folder, disk_offload_index)
    return disk_offload_index

