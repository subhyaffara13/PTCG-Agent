
def _transform_uuid_to_ordinals(candidates: list[str], uuids: list[str]) -> list[int]:
    r"""Given the set of partial uuids and list of known uuids builds a set of ordinals excluding ambiguous partials IDs."""

    def uuid_to_ordinal(candidate: str, uuids: list[str]) -> int:
        best_match = -1
        for idx, uuid in enumerate(uuids):
            if not uuid.startswith(candidate):
                continue
            # Ambiguous candidate
            if best_match != -1:
                return -1
            best_match = idx
        return best_match

    rc: list[int] = []
    for candidate in candidates:
        if torch.version.hip:
            candidate = candidate.replace(
                "GPU-", "", 1
            )  # Remove GPU-prefix to match amdsmi asic serial
        idx = uuid_to_ordinal(candidate, uuids)
        # First invalid ordinal stops parsing
        if idx < 0:
            break
        # Duplicates result in empty set
        if idx in rc:
            return cast(list[int], [])
        rc.append(idx)
    return rc

