from typing import Callable, Optional, Union

def inject_stateful_hyperparams(
    inner_factory: Callable[..., base.GradientTransformation],
    static_args: Union[str, Iterable[str]] = (),
    hyperparam_dtype: Optional[jnp.dtype] = None,
) -> Callable[..., base.GradientTransformationExtraArgs]:
  """Wrapper to injects stateful hyperparameters into GradientTransformations.

  Similar to `inject_hyperparams`, but supports both passing simple schedules
  that are function exclusively of the step count and also passing stateful
  schedules that rely on a complex internal state. The state updating can rely
  on additional information fed to gradient transformations via extra_args.

  Args:
    inner_factory: a function that returns the inner
      ``optax.GradientTransformation`` with dynamic hyperparameters.
    static_args: a string or iterable of strings specifying which callable
      parameters are not schedules. inject_hyperparams treats all callables as
      schedules by default, so if a hyperparameter is a non-schedule callable,
      you must specify that using this argument.
    hyperparam_dtype: Optional datatype override. If specified, all float
      hyperparameters will be cast to this type.

  Returns:
    A callable that returns a ``optax.GradientTransformation``. This callable
    accepts the same arguments as ``inner_factory``, except you may provide
    schedules in place of the constant arguments.

  .. deprecated:: 0.1.9
    Use :func:`inject_hyperparams` instead.
  """
  # raise deprecationwarning
  warnings.warn(
      'inject_stateful_hyperparams is deprecated, use inject_hyperparams'
      ' instead',
      DeprecationWarning,
  )
  return inject_hyperparams(inner_factory, static_args, hyperparam_dtype)

