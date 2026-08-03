import os
import sys
from typing import Any

def build_db(
    details: dict[str, dict[str, Any]], args: argparse.Namespace, version: str
) -> Database:
    if args.verbose:
        os.environ["FR_TRACE_VERBOSE_OUTPUT"] = "1"
    # temporary state used for building database
    entries = {}
    pg_config = {}
    version_by_ranks = {}
    for dump in details.values():
        rank = dump["rank"]
        entries[rank] = dump["entries"]
        version_by_ranks[rank] = dump["version"]
        pg_config[rank] = dump["pg_config"]

    # Ensure version is consistent across all ranks.
    check_version(version_by_ranks, version)
    entries = align_trace_from_beginning(entries)
    stack_id_trace_map: dict[str, int] = {}
    if args.just_print_entries:
        entries, stack_id_trace_map = add_stack_id_in_entries(entries)

    # flattened database
    groups, _groups, memberships, _memberships, _pg_guids = build_groups_memberships(
        pg_config
    )
    logger.debug("built groups, memberships")

    if args.just_print_entries:
        just_print_entries(
            entries, _groups, _memberships, _pg_guids, args, stack_id_trace_map
        )
        sys.exit(0)

    if not args.allow_incomplete_ranks:
        check_no_missing_dump_files(entries, memberships)

    tracebacks, collectives, nccl_calls = build_collectives(
        entries, _groups, _memberships, _pg_guids, version, args.mismatch_cap
    )
    logger.debug("built collectives, nccl_calls")
    if args.verbose:
        logger.debug("Groups")
        logger.debug(tabulate(groups, headers=Group._fields))
        logger.debug("Memberships")
        logger.debug(tabulate(memberships, headers=Membership._fields))
        logger.debug("Collectives")
        logger.debug(tabulate(collectives, headers=Collective._fields))
        logger.debug("NCCLCalls")
        logger.debug(tabulate(nccl_calls, headers=NCCLCall._fields))
    db = Database(
        tracebacks=tracebacks,
        collectives=collectives,
        ncclcalls=nccl_calls,
        groups=groups,
        memberships=memberships,
    )
    return db

