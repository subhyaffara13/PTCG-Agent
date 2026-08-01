
def as_torch_kernel(fn):
  """Makes a Mosaic GPU kernel callable with PyTorch tensors.

  Args:
    fn: A JAX function that invokes a Mosaic GPU kernel. Note that
      the implementation currently only supports functions that contain a
      single Mosaic GPU kernel invocation, without any other JAX API calls,
      e.g. from :mod:`jax.numpy`.

  Returns:
    A wrapper function that accepts PyTorch tensors as inputs and returns
    PyTorch tensors as outputs. The output tensors are allocated on the
    same device as the input tensors.

  Example::

      @plgpu.kernel(out_type=jax.ShapeDtypeStruct([128], jnp.int32)
      def kernel(x_gmem_ref, y_gmem_ref, o_gmem_ref):
        ...

      x = torch.arange(128, dtype=torch.int32, device="cuda")
      y = x * x
      out = plgpu.as_torch_kernel(kernel)(x, y)
  """
  @functools.wraps(fn)
  def wrapper(*args):
    in_structs = jax.tree.map(
        lambda arg: jax.ShapeDtypeStruct(
            # Drop the "torch." prefix from the dtype string, if present.
            arg.shape,
            str(arg.dtype).split(".")[-1],
        ),
        args,
    )
    return _compile_fn(fn, in_structs)(*args)

  return wrapper

