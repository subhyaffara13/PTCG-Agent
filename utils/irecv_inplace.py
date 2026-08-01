
def irecv_inplace(
    tensor: torch.Tensor,
    src: int,
    tag: int = 0,
    group: dist.ProcessGroup | None = None,
    group_src: int = -1,
):
    if group is None:
        group = dist.group.WORLD
    if group is None:
        raise AssertionError("group cannot be None")
    if group_src != -1:
        if src is not None:
            raise ValueError(
                "Cannot specify both 'src' and 'group_src' args as per eager impl"
            )
        global_src = c10d.get_global_rank(group, group_src)
    else:
        global_src = src
    group_name = _resolve_group_name(group)
    tensor = torch.ops._c10d_functional.irecv(tensor, global_src, tag, group_name)
    return _maybe_wrap_tensor(tensor)

