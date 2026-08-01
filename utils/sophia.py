
def sophia(
    learning_rate: base.ScalarOrSchedule,
    b1: jax.typing.ArrayLike = 0.965,
    b2: jax.typing.ArrayLike = 0.99,
    eps: jax.typing.ArrayLike = 1e-8,
    weight_decay: jax.typing.ArrayLike = 1e-4,
    weight_decay_mask: Optional[
        Union[Any, Callable[[base.Params], Any]]
    ] = None,
    gamma: jax.typing.ArrayLike = 0.01,
    clip_threshold: Optional[jax.typing.ArrayLike] = 1.0,
    update_interval: jax.typing.ArrayLike = 10,
    hessian_diagonal_fn: Union[
        base.GradientTransformation,
        base.GradientTransformationExtraArgs,
    ] = hutchinson_estimator_diag_hessian(),
    mu_dtype: Optional[Any] = None,
    verbose: bool = False,
    print_win_rate_every_n_steps: jax.typing.ArrayLike = 0,
) -> base.GradientTransformationExtraArgs:
  """Sophia optimizer.

  A separate GradientTransformation is required through the argument
  `hessian_diagonal_fn` to compute the diagonal of the Hessian. Any extra
  arguments required by the hessian_diagonal_fn's update function can be
  passed through sophia's update function as trailing keyword arguments
  (**kwargs). The default hessian_diagonal_fn is Hutchinson's estimator
  and needs the objective function as an extra argument, `obj_fn`.
  obj_fn must accept `params` as its only argument and return only a
  scalar (the loss).

  For example, assuming your experiment's loss function is
  `loss_fn(params, batch) -> loss, aux` that takes multiple arguments and
  returns multiple outputs, we must modify it to `loss_fn(params) -> loss`:

  `obj_fn = lambda params: loss_fn(params, batch)[0]`

  where `batch` is the current step's batch.

  Then it can be passed to sophia's update function (which will pass it to the
  hessian_diagonal_fn's update function):

  `updates, state = sophia.update(updates, state, params, obj_fn=sophia_obj_fn)`

  Optionally, you can write your own GradientTransformation to compute the
  hessian diagonal. Use this file's hutchinson_estimator_diag_hessian function
  as an example. If you are using more than one device, be sure the hessian
  diagonal function properly averages the hessian diagonal across devices.
  The default hessian_diagonal_fn does not do this, and would cause params to
  diverge from each other across devices if using pmap for example.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    b1: Exponential decay rate for the first moment estimates.
    b2: Exponential decay rate for the hessian diagonal estimates. Keep in mind
      effective `b2` is `1 - (1 - b2) / update_interval`, e.g. default `b2` of
      0.99 is effectively 0.999 because default `update_interval` is every 10.
    eps: Small constant to avoid division by zero.
    weight_decay: Rate at which to decay weights.
    weight_decay_mask: A tree with same structure as (or a prefix of) the params
      PyTree, or a Callable that returns such a pytree given the params/updates.
      The leaves should be booleans, `True` for leaves/subtrees you want to
      apply the transformation to, and `False` for those you want to skip.
    gamma: Normalizing constant for the hessian diagonal.
    clip_threshold: Threshold for clipping updates.
    update_interval: Interval for updating the hessian diagonal.
    hessian_diagonal_fn: GradientTransformation that computes the diagonal of
      the Hessian. Default is Hutchinson's estimator (sophia-h). If using more
      than one device, be sure this function properly averages the hessian
      diagonal across devices.
    mu_dtype: dtype of the first moment estimates.
    verbose: If True, print win rate every n steps.
    print_win_rate_every_n_steps: Print sophia win rate every n steps for
      diagnostic purposes. Authors state this value should stay between 0.1 and
      0.5 during training. If win rate is too low, try increasing `gamma`. 0 to
      turn off.

  Returns:
    optax.GradientTransformationExtraArgs

  References:
    Liu et al., `Sophia: A Scalable Stochastic Second-order Optimizer for
    Language Model Pre-training <https://arxiv.org/abs/2305.14342>`_, 2023

    `Levanter <https://www.github.com/stanford-crfm/levanter>`_

  .. note::
    We use a rademacher vector to estimate the diagonal of the Hessian, contrary
    to the original implementation which uses a normal random vector.
  """
  tx = [
      scale_by_sophia(
          b1=b1,
          b2=b2,
          eps=eps,
          gamma=gamma,
          clip_threshold=clip_threshold,
          update_interval=update_interval,
          hessian_diagonal_fn=hessian_diagonal_fn,
          mu_dtype=mu_dtype,
          verbose=verbose,
          print_win_rate_every_n_steps=print_win_rate_every_n_steps,
      ),
      _adding.add_decayed_weights(weight_decay, mask=weight_decay_mask),
      transform.scale_by_learning_rate(learning_rate),
  ]
  return combine.chain(*tx)

