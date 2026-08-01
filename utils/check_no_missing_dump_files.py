
def check_no_missing_dump_files(
    entries: dict[int, Any], memberships: list[Membership]
) -> None:
    all_ranks = {int(membership.global_rank) for membership in memberships}
    dumps_ranks = {int(key) for key in entries}
    missing = all_ranks - dumps_ranks
    if len(missing) != 0:
        raise AssertionError(f"Missing dump files from ranks {missing}")

