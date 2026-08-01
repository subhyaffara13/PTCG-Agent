
def solve_with_dependent(
    vars: list[TypeVarId],
    constraints: list[Constraint],
    original_vars: list[TypeVarId],
    originals: dict[TypeVarId, TypeVarLikeType],
) -> tuple[Solutions, list[TypeVarLikeType]]:
    """Solve set of constraints that may depend on each other, like T <: List[S].

    The whole algorithm consists of five steps:
      * Propagate via linear constraints and use secondary constraints to get transitive closure
      * Find dependencies between type variables, group them in SCCs, and sort topologically
      * Check that all SCC are intrinsically linear, we can't solve (express) T <: List[T]
      * Variables in leaf SCCs that don't have constant bounds are free (choose one per SCC)
      * Solve constraints iteratively starting from leaves, updating bounds after each step.
    """
    graph, lowers, uppers = transitive_closure(vars, constraints)

    dmap = compute_dependencies(vars, graph, lowers, uppers)
    sccs = list(strongly_connected_components(set(vars), dmap))
    if not all(check_linear(scc, lowers, uppers) for scc in sccs):
        return {}, []
    raw_batches = list(topsort(prepare_sccs(sccs, dmap)))

    free_vars = []
    free_solutions = {}
    for scc in raw_batches[0]:
        # If there are no bounds on this SCC, then the only meaningful solution we can
        # express, is that each variable is equal to a new free variable. For example,
        # if we have T <: S, S <: U, we deduce: T = S = U = <free>.
        if all(not lowers[tv] and not uppers[tv] for tv in scc):
            best_free = choose_free([originals[tv] for tv in scc], original_vars)
            if best_free:
                # TODO: failing to choose may cause leaking type variables,
                # we need to fail gracefully instead.
                free_vars.append(best_free.id)
                free_solutions[best_free.id] = best_free

    # Update lowers/uppers with free vars, so these can now be used
    # as valid solutions.
    for l, u in graph:
        if l in free_vars:
            lowers[u].add(free_solutions[l])
        if u in free_vars:
            uppers[l].add(free_solutions[u])

    # Flatten the SCCs that are independent, we can solve them together,
    # since we don't need to update any targets in between.
    batches = []
    for batch in raw_batches:
        next_bc = []
        for scc in batch:
            next_bc.extend(list(scc))
        batches.append(next_bc)

    solutions: dict[TypeVarId, Type | None] = {}
    for flat_batch in batches:
        res = solve_iteratively(flat_batch, graph, lowers, uppers)
        solutions.update(res)
    return solutions, [free_solutions[tv] for tv in free_vars]

