from typing import Any, Callable

def evaluate(
    environment: str | "Environment",
    agents: list[str | Callable | Agent] | None = None,
    configuration: dict[str, Any] | None = None,
    steps: list[list[dict[str, Any]]] | None = None,
    num_episodes: int = 1,
    debug: bool = False,
    state: list[dict[str, Any]] | None = None,
) -> list[list[float | None]]:
    """
    Evaluate and return the rewards of one or more episodes (environment and agents combo).

    Args:
        environment (str|Environment):
        agents (list):
        configuration (dict, optional):
        steps (list, optional):
        num_episodes (int=1, optional): How many episodes to execute (run until done).
        debug (bool=False, optional): Render print() statments to stdout
        state (optional)

    Returns:
        list of list of int: List of final rewards for all agents for all episodes.
    """
    if agents is None:
        agents = []
    if configuration is None:
        configuration = {}
    if steps is None:
        steps = []

    e = make(environment, configuration, steps=steps, debug=debug, state=state)
    rewards = [[] for i in range(num_episodes)]
    for i in range(num_episodes):
        last_state = e.run(agents)[-1]
        rewards[i] = [state.reward for state in last_state]
    return rewards


def evaluate(calcfc, x, m_nlcon, amat, bvec):
    """
    This function evaluates CALCFC at X, returning the objective function value and the
    constraint value. Nan/Inf are handled by a moderated extreme barrier.
    """

    # Sizes
    m_lcon = len(bvec) if bvec is not None else 0

    # Preconditions
    if DEBUGGING:
        # X should not contain NaN if the initial X does not contain NaN and the
        # subroutines generating # trust-region/geometry steps work properly so that
        # they never produce a step containing NaN/Inf.
        assert not any(np.isnan(x))

    #====================#
    # Calculation starts #
    #====================#

    constr = np.zeros(m_lcon + m_nlcon)
    if amat is not None:
        constr[:m_lcon] = matprod(x, amat.T) - bvec

    if any(np.isnan(x)):
        # Although this should not happen unless there is a bug, we include this case
        # for robustness.
        f = primasum(x)
        constr = np.ones(m_nlcon) * f
    else:
        f, constr[m_lcon:] = calcfc(moderatex(x))

        # Moderated extreme barrier: replace NaN/huge objective or constraint values
        # with a large but finite value. This is naive, and better approaches surely
        # exist.
        f = moderatef(f)
        constr[m_lcon:] = moderatec(constr[m_lcon:])

    #==================#
    # Calculation ends #
    #==================#

    # Postconditions
    if DEBUGGING:
        # With X not containing NaN, and with the moderated extreme barrier, F cannot
        # be NaN/+Inf, and CONSTR cannot be NaN/-Inf.
        assert not (np.isnan(f) or np.isposinf(f))
        assert not any(np.isnan(constr) | np.isposinf(constr))

    return f, constr


def evaluate(op, left_op, right_op, use_numexpr: bool = True):
    """
    Evaluate and return the expression of the op on left_op and right_op.

    Parameters
    ----------
    op : the actual operand
    left_op : left operand
    right_op : right operand
    use_numexpr : bool, default True
        Whether to try to use numexpr.
    """
    op_str = _op_str_mapping[op]
    if op_str is not None:
        if use_numexpr:
            # error: "None" not callable
            return _evaluate(op, op_str, left_op, right_op)  # type: ignore[misc]
    return _evaluate_standard(op, op_str, left_op, right_op)


def evaluate(f, *, allow_transpose: bool = True):
  def wrapped(*args, **kwargs):
    jaxpr, consts, _, out_tree = fuser_utils.make_jaxpr(f, *args, **kwargs)
    settings = CustomEvaluateSettings(allow_transpose=allow_transpose)
    flat_args = tree_util.tree_leaves(args)
    out_flat = _custom_evaluate_jaxpr(settings, jaxpr, consts, *flat_args)
    return tree_util.tree_unflatten(out_tree, out_flat)

  return wrapped

