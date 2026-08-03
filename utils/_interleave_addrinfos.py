import itertools

def _interleave_addrinfos(
    addrinfos: Sequence[AddrInfoType], first_address_family_count: int = 1
) -> list[AddrInfoType]:
    """Interleave list of addrinfo tuples by family."""
    # Group addresses by family
    addrinfos_by_family: defaultdict[int, list[AddrInfoType]] = defaultdict(list)
    for addr in addrinfos:
        addrinfos_by_family[addr[0]].append(addr)
    addrinfos_lists = list(addrinfos_by_family.values())

    reordered: list[AddrInfoType] = []
    if first_address_family_count > 1:
        reordered.extend(addrinfos_lists[0][: first_address_family_count - 1])
        del addrinfos_lists[0][: first_address_family_count - 1]
    reordered.extend(
        a
        for a in itertools.chain.from_iterable(itertools.zip_longest(*addrinfos_lists))
        if a is not None
    )
    return reordered

