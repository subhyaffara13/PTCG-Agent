
def report_registrations(verbose: bool = False) -> None:
    """Report the number (and optionally full list) of ops by registration method.

    Directly registered categories (mutually exclusive):
      - rule: ops registered via register_prop_rule
      - op_strategy: ops registered via register_op_strategy
      - single_dim_strategy: ops registered via register_single_dim_strategy

    Ops not in any of the above may still be supported at runtime via
    DecompShardingStrategy, which traces through the op's decomposition and
    propagates placements through the decomposed sub-ops.  Whether this
    actually works depends on every sub-op having a registered strategy.
    We report the decomposition_table entries as a separate (untested) count.
    """
    from torch._decomp import decomposition_table

    propagator = DTensor._op_dispatcher.sharding_propagator

    rule_ops = sorted(propagator.op_to_rules.keys(), key=str)
    strategy_ops = sorted(propagator.op_strategy_funcs.keys(), key=str)
    single_dim_ops = sorted(propagator.op_single_dim_strategy_funcs.keys(), key=str)

    directly_registered = (
        set(propagator.op_to_rules.keys())
        | set(propagator.op_strategy_funcs.keys())
        | set(propagator.op_single_dim_strategy_funcs.keys())
    )

    # Ops from the explicit decomposition table that aren't directly registered.
    # These *may* work via DecompShardingStrategy if all their sub-ops are
    # supported, but we can't verify that without tracing each one.
    decomp_only_ops = sorted(
        (op for op in decomposition_table if op not in directly_registered),
        key=str,
    )

    print("=" * 70)
    print("DTensor operator registration report")
    print("=" * 70)

    print("\nDirectly registered:")
    print(f"  rule (register_prop_rule):            {len(rule_ops):>4}")
    print(f"  op_strategy (register_op_strategy):   {len(strategy_ops):>4}")
    print(f"  single_dim_strategy:                  {len(single_dim_ops):>4}")
    print(f"  total:                                {len(directly_registered):>4}")

    print(f"\nDecomposition table (not directly registered): {len(decomp_only_ops)}")
    print(
        "  These ops have entries in torch._decomp.decomposition_table but no\n"
        "  direct DTensor strategy. They may work at runtime via\n"
        "  DecompShardingStrategy if all decomposed sub-ops are supported.\n"
        "  Additional ops beyond this count may also be reachable via CIA\n"
        "  (CompositeImplicitAutograd) decompositions."
    )

    if verbose:

        def _print_ops(label: str, ops: list) -> None:
            print(f"\n{label} ({len(ops)}):")
            for op in ops:
                print(f"  {op}")

        _print_ops("rule", rule_ops)
        _print_ops("op_strategy", strategy_ops)
        _print_ops("single_dim_strategy", single_dim_ops)
        _print_ops("decomp table (not directly registered)", decomp_only_ops)

