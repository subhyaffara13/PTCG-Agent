
def pop_addr_infos_interleave(
    addr_infos: list[AddrInfoType], interleave: int | None = None
) -> None:
    """
    Pop addr_info from the list of addr_infos by family up to interleave times.

    The interleave parameter is used to know how many addr_infos for
    each family should be popped of the top of the list.
    """
    if interleave is None:
        interleave = 1
    seen: dict[int, int] = {}
    kept: list[AddrInfoType] = []
    for addr_info in addr_infos:
        family = addr_info[0]
        count = seen.get(family, 0)
        if count >= interleave:
            kept.append(addr_info)
        seen[family] = count + 1
    addr_infos[:] = kept

