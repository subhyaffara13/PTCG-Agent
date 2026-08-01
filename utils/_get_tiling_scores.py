
def _get_tiling_scores(
    inductor_meta: dict[str, Any],
    size_hints: dict[str, int],
) -> dict[str, float]:
    """
    Retrieve the tiling scores, providing suitable defaults if they are missing.
    """
    return inductor_meta.get("tiling_scores") or dict.fromkeys(size_hints, 1)

