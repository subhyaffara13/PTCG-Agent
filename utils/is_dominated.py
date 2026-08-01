
def is_dominated(
    action,
    game_or_payoffs,
    player,
    mode=DominanceType.DOMINANCE_STRICT,
    tol=1e-7,
    return_mixture=False,
):
  """Determines whether a pure strategy is dominated by any mixture strategies.

  Args:
    action: index of an action for `player`
    game_or_payoffs: either a pyspiel matrix- or normal-form game, or a payoff
      tensor for `player` with ndim == number of players
    player: index of the player (an integer)
    mode: dominance criterion: strict, weak, or very weak
    tol: tolerance
    return_mixture: whether to return the dominating strategy if one exists

  Returns:
    If `return_mixture`:
      a dominating mixture strategy if one exists, or `None`.
      the strategy is provided as a 1D numpy array of mixture weights.
    Otherwise: True if a dominating strategy exists, False otherwise.
  """
  # For more detail, please refer to Sec 4.5.2 of Shoham & Leyton-Brown, 2009:
  # Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations
  # http://www.masfoundations.org/mas.pdf
  assert mode in (
      DominanceType.DOMINANCE_STRICT,
      DominanceType.DOMINANCE_VERY_WEAK,
      DominanceType.DOMINANCE_WEAK,
  )
  payoffs = (
      utils.game_payoffs_array(game_or_payoffs)[player]
      if isinstance(game_or_payoffs, pyspiel.NormalFormGame)
      else np.asarray(game_or_payoffs, dtype=np.float64)
  )

  # Reshape payoffs so rows correspond to `player` and cols to the joint action
  # of all other players
  payoffs = np.moveaxis(payoffs, player, 0)
  payoffs = payoffs.reshape((payoffs.shape[0], -1))
  num_rows, num_cols = payoffs.shape

  lp = LinearProgram(ObjectiveType.OBJ_MAX)

  # One var for every row probability, fixed to 0 if inactive
  for r in range(num_rows):
    if r == action:
      lp.add_or_reuse_variable(r, lb=0, ub=0)
    else:
      lp.add_or_reuse_variable(r, lb=0)

  # For the strict LP we normalize the payoffs to be strictly positive
  if mode == DominanceType.DOMINANCE_STRICT:
    to_subtract = payoffs.min() - 1
  else:
    to_subtract = 0
    # For non-strict LPs the probabilities must sum to 1
    lp.add_or_reuse_constraint(num_cols, ConstraintType.CONS_TYPE_EQ)
    lp.set_cons_rhs(num_cols, 1)
    for r in range(num_rows):
      if r != action:
        lp.set_cons_coeff(num_cols, r, 1)

  # The main dominance constraint
  for c in range(num_cols):
    lp.add_or_reuse_constraint(c, ConstraintType.CONS_TYPE_GEQ)
    lp.set_cons_rhs(c, payoffs[action, c] - to_subtract)
    for r in range(num_rows):
      if r != action:
        lp.set_cons_coeff(c, r, payoffs[r, c] - to_subtract)

  if mode == DominanceType.DOMINANCE_STRICT:
    # Minimize sum of probabilities
    for r in range(num_rows):
      if r != action:
        lp.set_obj_coeff(r, -1)
    mixture = lp.solve()
    if mixture is not None and np.sum(mixture) < 1 - tol:
      mixture = mixture / np.sum(mixture)
    else:
      mixture = None

  if mode == DominanceType.DOMINANCE_VERY_WEAK:
    # Check feasibility
    mixture = lp.solve()

  if mode == DominanceType.DOMINANCE_WEAK:
    # Check feasibility and whether there's any advantage
    for r in range(num_rows):
      lp.set_obj_coeff(r, payoffs[r].sum())
    mixture = lp.solve()
    if mixture is not None:
      if (np.dot(mixture, payoffs) - payoffs[action]).sum() <= tol:
        mixture = None

  return mixture if return_mixture else (mixture is not None)

