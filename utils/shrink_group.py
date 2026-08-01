
def shrink_group(
    ranks_to_exclude: list[int],
    group: ProcessGroup | None = None,
    shrink_flags: int = SHRINK_DEFAULT,
    pg_options: Any | None = None,
) -> ProcessGroup:
    """
    Shrinks a process group by excluding specified ranks.

    Creates and returns a new, smaller process group comprising only the ranks
    from the original group that were not in the ``ranks_to_exclude`` list.

    Args:
        ranks_to_exclude (List[int]): A list of ranks from the original
            ``group`` to exclude from the new group.
        group (ProcessGroup, optional): The process group to shrink. If ``None``,
            the default process group is used. Defaults to ``None``.
        shrink_flags (int, optional): Flags to control the shrinking behavior.
            Can be ``SHRINK_DEFAULT`` (default) or ``SHRINK_ABORT``.
            ``SHRINK_ABORT`` will attempt to terminate ongoing operations
            in the parent communicator before shrinking.
            Defaults to ``SHRINK_DEFAULT``.
        pg_options (ProcessGroupOptions, optional): Backend-specific options to apply
            to the shrunken process group. If provided, the backend will use
            these options when creating the new group. If omitted, the new group
            inherits defaults from the parent.

    Returns:
        ProcessGroup: a new group comprised of the remaining ranks. If the
        default group was shrunk, the returned group becomes the new default group.

    Raises:
        TypeError: if the group’s backend does not support shrinking.
        ValueError: if ``ranks_to_exclude`` is invalid (empty, out of bounds,
        duplicates, or excludes all ranks).
        RuntimeError: if an excluded rank calls this function or the backend
        fails the operation.

    Notes:
        - Only non-excluded ranks should call this function; excluded ranks
          must not participate in the shrink operation.
        - Shrinking the default group destroys all other process groups since
          rank reassignment makes them inconsistent.
    """
    # Step 1: Validate input parameters with comprehensive error checking
    _validate_shrink_inputs(ranks_to_exclude, shrink_flags)

    # Step 2: Get target group and essential properties
    target_group_info = _prepare_shrink_target_group(group)

    # Step 3: Validate backend requirements and availability
    backend_impl = _validate_shrink_backend_requirements(target_group_info)

    # Step 4: Validate ranks against group and check for duplicates
    excluded_ranks_set = _validate_and_process_excluded_ranks(
        ranks_to_exclude, target_group_info
    )

    # Step 5: Execute the actual shrink operation (backend-specific)
    new_backend = backend_impl.shrink(
        sorted(excluded_ranks_set),
        shrink_flags,
        pg_options if pg_options is not None else None,
    )

    # Step 6: Handle cleanup and creation of new process group
    target_group_info["pg_options_override"] = pg_options
    return _finalize_shrunk_group(target_group_info, excluded_ranks_set, new_backend)

