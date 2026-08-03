from typing import List

def meta_loss(opt_params, net_apply, payoff, steps, rng):
  """Meta loss function."""

  regret_sum_x = np.zeros(shape=[FLAGS.batch_size, 1, FLAGS.num_actions])
  regret_sum_y = np.zeros(shape=[FLAGS.batch_size, 1, FLAGS.num_actions])
  total_loss = 0

  @jax.jit
  def body_fun(s, total_loss):
    nonlocal regret_sum_x
    nonlocal regret_sum_y
    x = net_apply(opt_params, rng, regret_sum_x / (s + 1))
    y = net_apply(opt_params, rng, regret_sum_y / (s + 1))

    strategy_x = jax.nn.softmax(x)
    strategy_y = jnp.transpose(jax.nn.softmax(y), [0, 2, 1])

    values_x = jnp.matmul(payoff, strategy_y)
    values_y = -jnp.matmul(strategy_x, payoff)

    value_x = jnp.matmul(jnp.matmul(strategy_x, payoff), strategy_y)
    value_y = -value_x

    curren_regret_x = values_x - value_x
    curren_regret_y = values_y - value_y
    curren_regret_x = jnp.transpose(curren_regret_x, [0, 2, 1])

    regret_sum_x += curren_regret_x
    regret_sum_y += curren_regret_y

    current_loss = jnp.max(
        jax.numpy.concatenate([curren_regret_x, curren_regret_y], axis=2),
        axis=[1, 2])
    total_loss += current_loss
    return total_loss
  def fori_loop(lower, steps, body_fun, total_loss):
    val = total_loss
    for i in range(lower, steps):
      val = body_fun(i, total_loss)
    return val
  total_loss = fori_loop(0, steps, body_fun, total_loss)
  return jnp.mean(total_loss)


def meta_loss(opt_params, net_apply, payoff, steps):

  """Returns the meta learning loss value.

  Args:
    opt_params: Optimizer parameters.
    net_apply: Apply function.
    payoff: Payoff matrix.
    steps: Number of steps.

  Returns:
    Accumulated loss value over number of steps.

  """
  regret_sum_x = np.zeros(shape=[FLAGS.batch_size, 1, FLAGS.num_actions])
  regret_sum_y = np.zeros(shape=[FLAGS.batch_size, 1, FLAGS.num_actions])
  total_loss = 0
  step = 0

  @jax.jit
  def scan_body(carry, x):
    nonlocal regret_sum_x
    nonlocal regret_sum_y
    regret_sum_x, regret_sum_y, current_step, total_loss = carry
    x = net_apply(opt_params, None, regret_sum_x / (current_step + 1))
    y = net_apply(opt_params, None, regret_sum_y / (current_step + 1))

    strategy_x = jax.nn.softmax(x)
    strategy_y = jnp.transpose(jax.nn.softmax(y), [0, 2, 1])

    values_x = jnp.matmul(payoff, strategy_y)  # val_x = payoff * st_y
    values_y = -jnp.matmul(strategy_x, payoff)  # val_y = -1 * payoff * st_x

    value_x = jnp.matmul(jnp.matmul(strategy_x, payoff), strategy_y)
    value_y = -value_x

    curren_regret_x = values_x - value_x
    curren_regret_y = values_y - value_y
    curren_regret_x = jnp.transpose(curren_regret_x, [0, 2, 1])

    regret_sum_x += curren_regret_x
    regret_sum_y += curren_regret_y

    current_loss = jnp.mean(jnp.max(
        jax.numpy.concatenate([curren_regret_x, curren_regret_y], axis=2),
        axis=[1, 2]), axis=-1)
    total_loss += current_loss
    current_step += 1
    return (regret_sum_x, regret_sum_y, current_step, total_loss), None

  (regret_sum_x, regret_sum_y, step, total_loss), _ = jax.lax.scan(
      scan_body,
      (regret_sum_x, regret_sum_y, step, total_loss),
      None,
      length=steps,
  )

  return total_loss


def meta_loss(net_params: Params, cfvalues: np.ndarray,
              net_apply: ApplyFn, steps: int, num_all_actions: int,
              infosets: List[InfostateNode],
              infostate_map: InfostateMapping,
              batch_size: int,
              key: hk.PRNGSequence,
              use_infostate_representation: bool = True) -> float:
  """Meta learning loss function.

  Args:
    net_params: Network parameters.
    cfvalues: Counterfactual values.
    net_apply: Haiku apply function.
    steps: Number of unrolling steps.
    num_all_actions: Number of actions.
    infosets: List of information states.
    infostate_map: Mapping from information state string to information state
      node.
    batch_size: Batch size.
    key: Pseudo random number.
    use_infostate_representation: Boolean value indicating if information state
      representation is used as part of input.

  Returns:
    Mean meta learning loss value.
  """
  regret_sum = np.zeros(shape=[batch_size, 1, num_all_actions])
  total_loss = 0
  step = 0
  infostate_str_one_hot = jnp.expand_dims(
      jnp.array([
          jax.nn.one_hot(infostate_map[infoset.infostate_string],
                         len(infostate_map)) for infoset in infosets
      ]),
      axis=1)

  def scan_body(carry, x):
    del x  # Unused
    regret_sum, current_step, total_loss = carry
    average_regret = regret_sum / (current_step + 1)

    if use_infostate_representation:
      net_input = jnp.concatenate((average_regret, infostate_str_one_hot),
                                  axis=-1)
    else:
      net_input = average_regret
    next_step_x = jax.jit(net_apply)(net_params, key, net_input)
    strategy = jax.nn.softmax(next_step_x)

    value = jnp.matmul(
        jnp.array(cfvalues), jnp.transpose(strategy, axes=[0, 2, 1]))
    curren_regret = jnp.array(cfvalues) - value
    regret_sum += jnp.expand_dims(jnp.mean(curren_regret, axis=1), axis=1)
    current_loss = jnp.mean(
        jnp.max(
            jax.numpy.concatenate(
                [regret_sum,
                 jnp.zeros(shape=[batch_size, 1, 1])],
                axis=-1),
            axis=-1))
    total_loss += current_loss
    current_step += 1
    return (regret_sum, current_step, total_loss), None

  (regret_sum, step, total_loss), _ = jax.lax.scan(
      scan_body, (regret_sum, step, total_loss), None, length=steps)
  return total_loss

