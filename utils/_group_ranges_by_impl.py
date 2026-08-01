
def _group_ranges_by_impl(
    range_to_best_impl: dict[RangeBounds, ImplConfig],
) -> list[RangeImplGroup]:
    """Group ranges by implementation using semantic identity (name + kwargs)."""
    from torch._inductor import config

    if not range_to_best_impl:
        return []

    # Test mode: skip grouping to force torch.cond dispatch path
    if config.test_configs.force_no_impl_grouping:
        log.info("Test mode: skipping impl grouping, each range is separate group")
        groups = []
        for range_bounds, impl_config in sorted(
            range_to_best_impl.items(), key=lambda x: x[0].start
        ):
            group = RangeImplGroup(impl_config)
            group.add_range(range_bounds)
            groups.append(group)
        return groups

    # Group ranges by impl_config (uses __hash__ and __eq__ based on semantic identity)
    impl_to_group: dict[ImplConfig, RangeImplGroup] = {}

    for range_bounds, impl_config in range_to_best_impl.items():
        if impl_config not in impl_to_group:
            impl_to_group[impl_config] = RangeImplGroup(impl_config)
        impl_to_group[impl_config].add_range(range_bounds)

    # Sort groups by first range start for deterministic codegen
    groups = sorted(impl_to_group.values(), key=lambda g: g.ranges[0].start)

    # Log grouping info
    original_count = len(range_to_best_impl)
    grouped_count = len(groups)

    if grouped_count < original_count:
        log.info(
            "Implementation grouping: reduced from %d ranges to %d impl groups",
            original_count,
            grouped_count,
        )

    return groups

