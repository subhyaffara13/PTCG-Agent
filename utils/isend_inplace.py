
def isend_inplace(
    tensor: torch.Tensor,
    dst: int,
    tag: int = 0,
    group: dist.ProcessGroup | None = None,
    group_dst: int = -1,
):
    if group is None:
        group = dist.group.WORLD
    if group is None:
        raise AssertionError("group cannot be None")
    if group_dst != -1:
        if dst is not None:
            raise ValueError(
                "Cannot specify both 'dst' and 'group_dst' args as per eager impl"
            )
        global_dst = c10d.get_global_rank(group, group_dst)
    else:
        global_dst = dst

    group_name = _resolve_group_name(group)
    tensor = torch.ops._c10d_functional.isend(tensor, global_dst, tag, group_name)
    if _are_we_tracing():
        return tensor
    return _maybe_wrap_tensor(tensor)

