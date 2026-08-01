
def monitor(f, input='print', output='print'):
    """
    Returns a wrapped copy of *f* that monitors evaluation by calling
    *input* with every input (*args*, *kwargs*) passed to *f* and
    *output* with every value returned from *f*. The default action
    (specify using the special string value ``'print'``) is to print
    inputs and outputs to stdout, along with the total evaluation
    count::

        >>> from mpmath import *
        >>> mp.dps = 5; mp.pretty = False
        >>> diff(monitor(exp), 1)   # diff will eval f(x-h) and f(x+h)
        in  0 (mpf('0.99999999906867742538452148'),) {}
        out 0 mpf('2.7182818259274480055282064')
        in  1 (mpf('1.0000000009313225746154785'),) {}
        out 1 mpf('2.7182818309906424675501024')
        mpf('2.7182808')

    To disable either the input or the output handler, you may
    pass *None* as argument.

    Custom input and output handlers may be used e.g. to store
    results for later analysis::

        >>> mp.dps = 15
        >>> input = []
        >>> output = []
        >>> findroot(monitor(sin, input.append, output.append), 3.0)
        mpf('3.1415926535897932')
        >>> len(input)  # Count number of evaluations
        9
        >>> print(input[3]); print(output[3])
        ((mpf('3.1415076583334066'),), {})
        8.49952562843408e-5
        >>> print(input[4]); print(output[4])
        ((mpf('3.1415928201669122'),), {})
        -1.66577118985331e-7

    """
    if not input:
        input = lambda v: None
    elif input == 'print':
        incount = [0]
        def input(value):
            args, kwargs = value
            print("in  %s %r %r" % (incount[0], args, kwargs))
            incount[0] += 1
    if not output:
        output = lambda v: None
    elif output == 'print':
        outcount = [0]
        def output(value):
            print("out %s %r" % (outcount[0], value))
            outcount[0] += 1
    def f_monitored(*args, **kwargs):
        input((args, kwargs))
        v = f(*args, **kwargs)
        output(v)
        return v
    return f_monitored


def monitor(
    measures: dict[
        str,
        base.GradientTransformationExtraArgs
        | Callable[[base.Updates], base.ArrayTree],
    ],
):
  """Monitors stateful measurements of updates in a chain.

  Extends func::`optax.snapshot` to use stateful measurements, such as using
  exponential moving average.

  Args:
    measures: A dictionary of measurement names to gradient transformations
      capturing them.

  Returns:
    A gradient transformation that captures measurements defined by the user.

  Examples:
    >>> import optax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)
    >>> clip_thresh = 1.0
    >>> solver = optax.chain(
    ...     optax.sgd(learning_rate=0.1, momentum=0.9),
    ...     optax.monitor({
    ...         'norm_before_clip': optax.tree.norm,
    ...         'is_clipped_ema': optax.measure_with_ema(
    ...             lambda x: optax.tree.norm(x) > clip_thresh,
    ...             decay=0.9,
    ...         )
    ...     }),
    ...     optax.clip_by_global_norm(clip_thresh),
    ... )
    >>> params = jnp.array([1., 2., 3.])
    >>> state = solver.init(params)
    >>> for step in range(2):
    ...   grads = jax.grad(f)(params)
    ...   updates, state = solver.update(grads, state)
    ...   params = optax.apply_updates(params, updates)
    ...   norm_before_clip = optax.tree.get(state, 'norm_before_clip')
    ...   is_clipped_ema = optax.tree.get(state, 'is_clipped_ema')
    ...   print(f'{step=}, {norm_before_clip=:.2e}, {is_clipped_ema=:.2e}')
    step=0, norm_before_clip=7.48e-01, is_clipped_ema=0.00e+00
    step=1, norm_before_clip=1.27e+00, is_clipped_ema=5.26e-01

  .. versionadded: 0.2.7
  """

  measures_ = {}
  for measure_name, measure in measures.items():
    if callable(measure):
      measure_ = base.stateless(lambda u, _, m=measure: m(u))
      measures_[measure_name] = base.with_extra_args_support(measure_)
    else:
      measures_[measure_name] = base.with_extra_args_support(measure)
  measures = measures_
  measure_names = tuple(measures.keys())

  def init(params: base.Params) -> MonitorState:
    measurements = {}
    measure_states = []
    for measure_name in measure_names:
      measure_states.append(measures[measure_name].init(params))
    return MonitorState(measurements, tuple(measure_states))

  def update(
      updates: base.Updates,
      state: MonitorState,
      params: base.Params | None = None,
      **extra_args: dict[str, Any],
  ) -> tuple[base.Updates, MonitorState]:
    measurements = {}
    new_measure_states = []
    for i, measure_name in enumerate(measure_names):
      measurement, measure_state = measures[measure_name].update(
          updates,
          state.measure_states[i],
          params,
          **extra_args,
      )
      measurements[measure_name] = measurement
      new_measure_states.append(measure_state)
    return updates, MonitorState(measurements, tuple(new_measure_states))

  return base.GradientTransformationExtraArgs(init, update)

