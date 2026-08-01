
def remove_addr_infos(
    addr_infos: list[AddrInfoType],
    addr: tuple[str, int] | tuple[str, int, int, int],
) -> None:
    """
    Remove an address from the list of addr_infos.

    The addr value is typically the return value of
    sock.getpeername().
    """
    kept = [ai for ai in addr_infos if ai[-1] != addr]
    if len(kept) == len(addr_infos):
        # Slow path in case addr is formatted differently
        match_addr = _addr_tuple_to_ip_address(addr)
        kept = [
            ai for ai in addr_infos if _addr_tuple_to_ip_address(ai[-1]) != match_addr
        ]
    if len(kept) == len(addr_infos):
        raise ValueError(f"Address {addr} not found in addr_infos")
    addr_infos[:] = kept

