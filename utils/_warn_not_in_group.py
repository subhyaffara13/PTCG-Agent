
def _warn_not_in_group(op_name) -> None:
    global_rank = -1 if GroupMember.WORLD is None else GroupMember.WORLD.rank()
    warnings.warn(
        f"Running {op_name} on global rank {global_rank} which does not "
        "belong to the given group.",
        stacklevel=2,
    )

