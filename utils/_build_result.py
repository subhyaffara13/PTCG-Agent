
def _build_result(pb, penalty, success, status, n_iter, options):
    """
    Build the result of the optimization process.
    """
    # Build the result.
    x, fun, maxcv = pb.best_eval(penalty)
    success = success and np.isfinite(fun) and np.isfinite(maxcv)
    if status not in [ExitStatus.TARGET_SUCCESS, ExitStatus.FEASIBLE_SUCCESS]:
        success = success and maxcv <= options[Options.FEASIBILITY_TOL]
    result = OptimizeResult()
    result.message = {
        ExitStatus.RADIUS_SUCCESS: "The lower bound for the trust-region "
                                   "radius has been reached",
        ExitStatus.TARGET_SUCCESS: "The target objective function value has "
                                   "been reached",
        ExitStatus.FIXED_SUCCESS: "All variables are fixed by the bound "
                                  "constraints",
        ExitStatus.CALLBACK_SUCCESS: "The callback requested to stop the "
                                     "optimization procedure",
        ExitStatus.FEASIBLE_SUCCESS: "The feasibility problem received has "
                                     "been solved successfully",
        ExitStatus.MAX_EVAL_WARNING: "The maximum number of function "
                                     "evaluations has been exceeded",
        ExitStatus.MAX_ITER_WARNING: "The maximum number of iterations has "
                                     "been exceeded",
        ExitStatus.INFEASIBLE_ERROR: "The bound constraints are infeasible",
        ExitStatus.LINALG_ERROR: "A linear algebra error occurred",
    }.get(status, "Unknown exit status")
    result.success = success
    result.status = status.value
    result.x = pb.build_x(x)
    result.fun = fun
    result.maxcv = maxcv
    result.nfev = pb.n_eval
    result.nit = n_iter
    if options[Options.STORE_HISTORY]:
        result.fun_history = pb.fun_history
        result.maxcv_history = pb.maxcv_history

    # Print the result if requested.
    if options[Options.VERBOSE]:
        _print_step(
            result.message,
            pb,
            result.x,
            result.fun,
            result.maxcv,
            result.nfev,
            result.nit,
        )
    return result


def _build_result(state: State[RT, CT, KT]) -> Result[RT, CT, KT]:
    mapping = state.mapping
    all_keys: dict[int, KT | None] = {id(v): k for k, v in mapping.items()}
    all_keys[id(None)] = None

    graph: DirectedGraph[KT | None] = DirectedGraph()
    graph.add(None)  # Sentinel as root dependencies' parent.

    connected: set[KT | None] = {None}
    for key, criterion in state.criteria.items():
        if not _has_route_to_root(state.criteria, key, all_keys, connected):
            continue
        if key not in graph:
            graph.add(key)
        for p in criterion.iter_parent():
            try:
                pkey = all_keys[id(p)]
            except KeyError:
                continue
            if pkey not in graph:
                graph.add(pkey)
            graph.connect(pkey, key)

    return Result(
        mapping={k: v for k, v in mapping.items() if k in connected},
        graph=graph,
        criteria=state.criteria,
    )

