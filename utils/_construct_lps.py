
def _construct_lps(
    state: pyspiel.State,
    infosets,
    infoset_actions: dict,
    infoset_action_maps: dict,
    chance_reach: float,
    lps: list[lp_solver.LinearProgram],
    parent_is_keys: dict[str],
    parent_isa_keys: dict[str],
    slack_variables: bool = False,
    depths: list = None,
    eps=0.0,
):
  """Build the linear programs recursively from this state.

  Args:
    state: an open spiel state (root of the game tree)
    infosets: a list of dicts, one per player, that maps infostate to an id. The
      dicts are filled by this function and should initially only contain root
      values.
    infoset_actions: a list of dicts, one per player, that maps a string of
      (infostate, action) pair to an id. The dicts are filled by this function
      and should initially only contain the root values
    infoset_action_maps: a list of dicts, one per player, that maps each
      info_state to a list of (infostate, action) string
    chance_reach: the contribution of chance's reach probability (should start
      at 1).
    lps: a list of linear programs, one per player. The first one will be
      constructred as in Eq (8) of Koller, Megiddo and von Stengel. The second
      lp is Eq (9). Initially these should contain only the root-level
      constraints and variables.
    parent_is_keys: a list of parent information state keys for this state
    parent_isa_keys: a list of parent (infostate, action) keys
    slack_variables: whether to use slack variables
    depths: a list of actions commited before the infoset by a player
    eps: eps: perturbation strength (0.0 = classic KMvS Nash, 1e-8 = sequential
      eq.)
  """
  if state.is_terminal():
    returns = state.returns()
    # Left-most term of: -Ay + E^T p (- u)>= 0
    lps[0].add_or_reuse_constraint(
        parent_isa_keys[0], lp_solver.ConstraintType.CONS_TYPE_GEQ
    )
    lps[0].add_to_cons_coeff(
        parent_isa_keys[0], parent_isa_keys[1], -1.0 * returns[0] * chance_reach
    )
    # Right-most term of: -Ay + E^T p (+ v) >= 0
    lps[0].set_cons_coeff(parent_isa_keys[0], parent_is_keys[0], 1.0)

    # Left-most term of: x^T (-A) - q^T F <= 0
    lps[1].add_or_reuse_constraint(
        parent_isa_keys[1], lp_solver.ConstraintType.CONS_TYPE_LEQ
    )
    lps[1].add_to_cons_coeff(
        parent_isa_keys[1], parent_isa_keys[0], -1.0 * returns[0] * chance_reach
    )
    # Right-most term of: x^T (-A) - q^T F <= 0
    lps[1].set_cons_coeff(parent_isa_keys[1], parent_is_keys[1], -1.0)
    return

  if state.is_chance_node():
    for action, prob in state.chance_outcomes():
      new_state = state.child(action)
      _construct_lps(
          new_state,
          infosets,
          infoset_actions,
          infoset_action_maps,
          prob * chance_reach,
          lps,
          parent_is_keys,
          parent_isa_keys,
          slack_variables,
          depths,
          eps,
      )
    return

  player = state.current_player()
  info_state = state.information_state_string(player)
  legal_actions = state.legal_actions(player)

  # p and q variables, inequality constraints, and part of equality constraints
  if player == 0:
    # p
    lps[0].add_or_reuse_variable(info_state)
    # -Ay + E^T p >= 0
    lps[0].add_or_reuse_constraint(
        parent_isa_keys[0], lp_solver.ConstraintType.CONS_TYPE_GEQ
    )
    lps[0].set_cons_coeff(parent_isa_keys[0], parent_is_keys[0], 1.0)
    lps[0].set_cons_coeff(parent_isa_keys[0], info_state, -1.0)
    # x^T E^T = e^T
    lps[1].add_or_reuse_constraint(
        info_state, lp_solver.ConstraintType.CONS_TYPE_EQ
    )
    lps[1].set_cons_coeff(info_state, parent_isa_keys[0], -1.0)
  else:
    # q
    lps[1].add_or_reuse_variable(info_state)
    # x^T (-A) - q^T F <= 0
    lps[1].add_or_reuse_constraint(
        parent_isa_keys[1], lp_solver.ConstraintType.CONS_TYPE_LEQ
    )
    lps[1].set_cons_coeff(parent_isa_keys[1], parent_is_keys[1], -1.0)
    lps[1].set_cons_coeff(parent_isa_keys[1], info_state, 1.0)
    # -Fy = -f
    lps[0].add_or_reuse_constraint(
        info_state, lp_solver.ConstraintType.CONS_TYPE_EQ
    )
    lps[0].set_cons_coeff(info_state, parent_isa_keys[1], -1.0)

  # Add to the infostate maps
  if info_state not in infosets[player]:
    infosets[player][info_state] = len(infosets[player])
  if info_state not in infoset_action_maps[player]:
    infoset_action_maps[player][info_state] = []

  new_parent_is_keys = parent_is_keys[:]
  new_parent_is_keys[player] = info_state

  for action in legal_actions:
    isa_key = info_state + _DELIMITER + str(action)
    if isa_key not in infoset_actions[player]:
      infoset_actions[player][isa_key] = len(infoset_actions[player])
    if isa_key not in infoset_action_maps[player][info_state]:
      infoset_action_maps[player][info_state].append(isa_key)

    # x and y variables, and finish equality constraints coeff
    # x ≥ k_ε and y ≥ l_ε to force sequential equilibrium
    # This is exactly equivalent to introducing explicit slack variables u/v
    # in the dual (the solver handles the u/v automatically).
    lb = eps ** (depths[player] + 1)
    # The variable that's created here is the realisation weight
    # *after* an action, which becomes the reach to the child infoset
    # (d_u for the child infoset = actions so far + 1).
    lps[1 - player].add_or_reuse_variable(isa_key, lb=lb)  # x or y
    # x^T E^T = e^T or -Fy = -f
    lps[1 - player].set_cons_coeff(info_state, isa_key, 1.0)

    if slack_variables:
      label = ("u_" if player == 0 else "v_") + isa_key
      if player == 0:
        lps[0].add_or_reuse_variable(label, lb=0.0)
        # Rightmost term of -Ay + E^T p (- u)>= 0
        lps[0].add_or_reuse_constraint(
            isa_key, lp_solver.ConstraintType.CONS_TYPE_GEQ
        )
        lps[0].set_cons_coeff(isa_key, label, -1.0)
        # Eq (2.4) min ... + - (k_eps^T u)
        lps[0].set_obj_coeff(label, -lb)
      else:
        lps[1].add_or_reuse_variable(label, lb=0.0)
        # Rightmost term of -x^T(-A) + q^T F + v  <= 0
        lps[1].add_or_reuse_constraint(
            isa_key, lp_solver.ConstraintType.CONS_TYPE_LEQ
        )
        lps[1].set_cons_coeff(isa_key, label, 1.0)
        # Eq (2.5) max ... + (l_eps^T v)
        lps[1].set_obj_coeff(label, lb)

    new_depths = depths[:]
    new_depths[player] += 1  # for the child infose

    new_parent_isa_keys = parent_isa_keys[:]
    new_parent_isa_keys[player] = isa_key

    new_state = state.child(action)
    _construct_lps(
        new_state,
        infosets,
        infoset_actions,
        infoset_action_maps,
        chance_reach,
        lps,
        new_parent_is_keys,
        new_parent_isa_keys,
        slack_variables,
        new_depths,
        eps,
    )

