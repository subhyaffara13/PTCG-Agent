
def find_unique_signatures(sigs: Sequence[Sig]) -> list[Sig]:
    """Remove names with duplicate found signatures."""
    sig_map: MutableMapping[str, list[str]] = {}
    for name, sig in sigs:
        sig_map.setdefault(name, []).append(sig)

    result = []
    for name, name_sigs in sig_map.items():
        if len(set(name_sigs)) == 1:
            result.append((name, name_sigs[0]))
    return sorted(result)

