
def format_verification_infos(
    verification_infos: list[_verification.VerificationInfo],
) -> str:
    """Format the verification result.

    Args:
        verification_infos: The verification result.

    Returns:
        The formatted verification result.
    """
    return "\n".join(
        f"`{info.name}`: `max_abs_diff={info.max_abs_diff:e}`, `max_rel_diff={info.max_rel_diff:e}`, "
        f"`abs_diff_hist={info.abs_diff_hist}`, `rel_diff_hist={info.rel_diff_hist}`"
        for info in verification_infos
    )

