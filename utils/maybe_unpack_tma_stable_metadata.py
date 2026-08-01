
def maybe_unpack_tma_stable_metadata(
    tma_meta: TMAExperimentalMetadata | TMAStableMetadata,
) -> tuple[list[IntLikeType]] | None:
    if not tma_meta or len(tma_meta) != 2:
        return None
    if tma_meta[0] == "stable":
        return tma_meta[1]  # type: ignore[return-value]
    return None

