
def _should_lower_as_one_shot_all_reduce(
    inp: ir.TensorBox,
    reduce_op: str,
    group_name: "torch.distributed.distributed_c10d.GroupName",
):
    from torch.distributed._symmetric_memory import is_symm_mem_enabled_for_group

    inp_size = inp.get_numel() * inp.get_dtype().itemsize
    return (
        config._collective.auto_select
        and is_symm_mem_enabled_for_group(group_name)
        and can_realize_as_comm_buffer(inp, ir.CommBufferType.SYMM_MEM)
        and reduce_op == "sum"
        and inp_size <= config._collective.one_shot_all_reduce_threshold_bytes
    )

