import functools
from typing import Any, Optional, Union

def _fake_pmap(fn,
               axis_name: Optional[Any] = None,
               *,
               in_axes=0,
               static_broadcasted_argnums: Union[int, Iterable[int]] = (),
               jit_result: bool = False,
               fake_parallel_axis: bool = False,
               **unused_kwargs):
  """Fake implementation of pmap using vmap."""

  if isinstance(static_broadcasted_argnums, int):
    static_broadcasted_argnums = (static_broadcasted_argnums,)
  if static_broadcasted_argnums and isinstance(in_axes, dict):
    raise NotImplementedError(
        'static_broadcasted_argnums with dict in_axes not supported.')

  fn_signature = inspect.signature(
      fn,
      # Disable 'follow wrapped' because we want the exact signature of fn,
      # not the signature of any function it might wrap.
      follow_wrapped=False)

  @functools.wraps(fn)
  def wrapped_fn(*args, **kwargs):
    # Convert kwargs to varargs
    # This is a workaround for vmapped functions not working with kwargs
    call_args = convert_to_varargs(fn_signature, *args, **kwargs)

    if static_broadcasted_argnums:
      # Make sure vmap does not try to map over `static_broadcasted_argnums`.
      if isinstance(in_axes, int):
        vmap_in_axes = [in_axes] * len(call_args)
      else:
        vmap_in_axes = list(in_axes)
      for argnum in static_broadcasted_argnums:
        vmap_in_axes[argnum] = None

      # To protect the arguments from `static_broadcasted_argnums`,
      # from turning into tracers (because of vmap), we capture the original
      # `call_args` and replace the passed in tracers with original values.
      original_call_args = call_args

      # A function passed to vmap, that will simply replace the static args
      # with their original values.
      def fn_without_statics(*args):
        args_with_original_statics = [
            orig_arg if i in static_broadcasted_argnums else arg
            for i, (arg, orig_arg) in enumerate(zip(args, original_call_args))
        ]
        return fn(*args_with_original_statics)

      # Make sure to avoid turning static args into tracers: Some python objects
      # might not survive vmap. Just replace with an unused constant.
      call_args = [
          1 if i in static_broadcasted_argnums else arg
          for i, arg in enumerate(call_args)
      ]

    else:
      vmap_in_axes = in_axes
      fn_without_statics = fn

    vmapped_fn = jax.vmap(
        fn_without_statics, in_axes=vmap_in_axes, axis_name=axis_name
    )
    if jit_result:
      vmapped_fn = jax.jit(vmapped_fn)

    if fake_parallel_axis:
      call_args = jax.tree_util.tree_map(
          lambda x: jnp.expand_dims(x, axis=0), call_args)

    output = vmapped_fn(*call_args)

    if fake_parallel_axis:
      output = jax.tree_util.tree_map(lambda x: jnp.squeeze(x, axis=0), output)

    return output

  return wrapped_fn

