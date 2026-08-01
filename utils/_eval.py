
def _eval(pb, framework, step, options):
    """
    Evaluate the objective and constraint functions.
    """
    if pb.n_eval >= options[Options.MAX_EVAL]:
        raise MaxEvalError
    x_eval = framework.x_best + step
    fun_val, cub_val, ceq_val = pb(x_eval, framework.penalty)
    r_val = pb.maxcv(x_eval, cub_val, ceq_val)
    if (
        fun_val <= options[Options.TARGET]
        and r_val <= options[Options.FEASIBILITY_TOL]
    ):
        raise TargetSuccess
    if pb.is_feasibility and r_val <= options[Options.FEASIBILITY_TOL]:
        raise FeasibleSuccess
    return fun_val, cub_val, ceq_val

