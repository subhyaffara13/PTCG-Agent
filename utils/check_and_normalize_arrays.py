
def check_and_normalize_arrays(
    fn: None = ...,
    *,
    strict: bool = ...,
) -> Callable[[_Fn], _Fn]:
  ...


def check_and_normalize_arrays(
    fn: _Fn = ...,
    *,
    strict: bool = ...,
) -> _Fn:
  ...


def check_and_normalize_arrays(fn=None, *, strict: bool = True):
  """Check and normalize arrays.

  This function:

  * Validate that the dtype/shape input arrays match the typing annotations
  * Normalize np, jnp, tf types to be consistent
  * Add an optional `xnp` argument to convert input arrays to np/jnp/tnp.

  See doc at: https://github.com/google/etils/blob/main/etils/array_types/README.md

  Example:

  ```python
  @enp.check_and_normalize_arrays(strict=False)
  def add(x: FloatArray[...], y: FloatArray[...]) -> y: FloatArray[...]:
    return x + y

  # Inside the function, `np` normalized to `jnp`
  add(np.array(1.), jnp.array(2.)) == jnp.array(3.)

  # strict=False, so `list` accepted and normalized to `xnp`
  add(jnp.array(1.), [1., 2., 3.]) == jnp.array([2., 3., 4.])
  ```

  Example with an explicit `xnp` argument, which automatically passed to the
  wrapped function:

  ```python
  @enp.check_and_normalize_arrays(strict=False)
  def clip(x: Array, *, xnp: enp.NpModule = ...) -> y: Array:
    return xnp.clip(x, 0.0, 1.0)
  ```

  If present in the function signature, the `xnp` argument must be a
  keyword-only argument.

  Args:
    fn: The function to decorate. Arguments will be automatically infered.
    strict: If `False`, `fn` will also accept list, int,... in which case those
      are automatically converted to `xnp`

  Returns:
    fn: The decorated function, with dynamic shape checking
  """

  if fn is None:
    return functools.partial(check_and_normalize_arrays, strict=strict)

  fn._array_types_state = None  # pylint: disable=protected-access

  @functools.wraps(fn)
  def decorated_fn(*args, **kwargs):
    try:
      kwargs = dict(kwargs)
      xnp = kwargs.pop('xnp', None)

      # First time the function is called, precompute & cache the info
      if fn._array_types_state is None:  # pylint: disable=protected-access
        fn._array_types_state = _parse_signature(fn)  # pylint: disable=protected-access

      state: _FnSignatureCache = fn._array_types_state  # pylint: disable=protected-access

      # In case `xnp` do not have default value
      if state.has_xnp_kwargs:
        kwargs['xnp'] = ...
      bound_args = state.sig.bind(*args, **kwargs)

      # Filter the non-array args
      # TODO(epot): Should raise an error for non-optional when v is None
      array_args = {
          k: v
          for k, v in bound_args.arguments.items()
          if k in state.array_params and v is not None
      }

      # Extract the xnp (either explicitly passed, or auto-infered)
      xnp = xnp or _get_xnp(array_args, strict=strict)
      _maybe_set_tnp_casting(xnp)

      # Normalize all arrays:
      # * Convert to xnp
      # * Check dtype
      array_args = {
          k: state.array_params[k].asarray(v, xnp=xnp)
          for k, v in array_args.items()
      }

      # TODO(epot): Check the shape

      # Update the arguments after normalization
      bound_args.arguments.update(array_args)

      # Eventually add `xnp` kwarg
      if state.has_xnp_kwargs:
        bound_args.arguments['xnp'] = xnp
    except Exception as e:  # pylint: disable=broad-except
      epy.reraise(
          e,
          prefix=(
              f'@enp.check_and_normalize_arrays error for {fn.__qualname__}: '
          ),
      )

    return fn(*bound_args.args, **bound_args.kwargs)

  return decorated_fn

