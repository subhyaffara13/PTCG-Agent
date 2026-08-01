
def solve_iteratively(
    batch: list[TypeVarId], graph: Graph, lowers: Bounds, uppers: Bounds
) -> Solutions:
    """Solve transitive closure sequentially, updating upper/lower bounds after each step.

    Transitive closure is represented as a linear graph plus lower/upper bounds for each
    type variable, see transitive_closure() docstring for details.

    We solve for type variables that appear in `batch`. If a bound is not constant (i.e. it
    looks like T :> F[S, ...]), we substitute solutions found so far in the target F[S, ...]
    after solving the batch.

    Importantly, after solving each variable in a batch, we move it from linear graph to
    upper/lower bounds, this way we can guarantee consistency of solutions (see comment below
    for an example when this is important).
    """
    solutions = {}
    s_batch = set(batch)
    while s_batch:
        for tv in sorted(s_batch, key=lambda x: x.raw_id):
            if lowers[tv] or uppers[tv]:
                solvable_tv = tv
                break
        else:
            break
        # Solve each solvable type variable separately.
        s_batch.remove(solvable_tv)
        result = solve_one(lowers[solvable_tv], uppers[solvable_tv])
        solutions[solvable_tv] = result
        if result is None:
            # TODO: support backtracking lower/upper bound choices and order within SCCs.
            # (will require switching this function from iterative to recursive).
            continue

        # Update the (transitive) bounds from graph if there is a solution.
        # This is needed to guarantee solutions will never contradict the initial
        # constraints. For example, consider {T <: S, T <: A, S :> B} with A :> B.
        # If we would not update the uppers/lowers from graph, we would infer T = A, S = B
        # which is not correct.
        for l, u in graph.copy():
            if l == u:
                continue
            if l == solvable_tv:
                lowers[u].add(result)
                graph.remove((l, u))
            if u == solvable_tv:
                uppers[l].add(result)
                graph.remove((l, u))

    # We can update uppers/lowers only once after solving the whole SCC,
    # since uppers/lowers can't depend on type variables in the SCC
    # (and we would reject such SCC as non-linear and therefore not solvable).
    subs = {tv: s for (tv, s) in solutions.items() if s is not None}
    for tv in lowers:
        lowers[tv] = {expand_type(lt, subs) for lt in lowers[tv]}
    for tv in uppers:
        uppers[tv] = {expand_type(ut, subs) for ut in uppers[tv]}
    return solutions

