
def _as_torch_gpu_kernel(
    module_asm: bytes,
    in_shape: Iterable[object],
    out_shape: Iterable[object],
    inout_shape: Iterable[object] = (),
    *,
    unwrap_output_tuple: bool = False,
    _prepare_args = None,
    _prepare_results = None,
):
  flat_arg_types, expected_arg_treedef = jax.tree.flatten((*in_shape, *inout_shape))
  flat_out_types, _ = jax.tree.flatten(out_shape)
  out_treedef = jax.tree.structure((*out_shape, *inout_shape))

  launch, unload = _compile_as_torch_gpu_kernel(module_asm)
  # _compile_as_torch_gpu_kernel checks that this succeeds
  import torch  # pyrefly: ignore[missing-import]

  def as_torch_dtype(dtype):
    # torch contains NumPy-compatible dtypes in its top namespace
    return getattr(torch, np.dtype(dtype).name)

  def apply(*args):
    flat_args, arg_treedef = jax.tree.flatten(args)
    if arg_treedef != expected_arg_treedef:
      raise ValueError(
          f"Invalid argument structure: expected {expected_arg_treedef}, got"
          f" {arg_treedef}, ({args=})"
      )
    for arg, expected_ty in zip(flat_args, flat_arg_types):
      if arg.shape != expected_ty.shape:
        raise ValueError(
            f"Argument shape mismatch: expected {expected_ty.shape}, got"
            f" {arg.shape}"
        )
      if arg.dtype != as_torch_dtype(expected_ty.dtype):
        raise ValueError(
            "Argument dtype mismatch: expected"
            f" {as_torch_dtype(expected_ty.dtype)}, got {arg.dtype}"
        )

    # Construct a device pointer list like in the XLA calling convention
    buffers = (ctypes.c_void_p * (arg_treedef.num_leaves + out_treedef.num_leaves))()
    i = -1  # Define i in case there are no args
    device = 'cuda'
    for i, arg in enumerate(flat_args):
      buffers[i] = arg.data_ptr()
      device = arg.device
    flat_outs = []
    for i, t in enumerate(flat_out_types, i + 1):
      out = torch.empty(t.shape, dtype=as_torch_dtype(t.dtype), device=device)
      flat_outs.append(out)
      buffers[i] = out.data_ptr()
    if num_inout_args := jax.tree.structure(inout_shape).num_leaves:
      flat_outs += flat_args[-num_inout_args:]
    launch(buffers, device)
    out = jax.tree.unflatten(out_treedef, flat_outs)
    return out[0] if unwrap_output_tuple else out

  # Unload the compiled code when the Python function is destroyed.
  apply.destructor = weakref.ref(apply, lambda _weak_ref: unload)  # pyrefly: ignore[missing-attribute]

  return apply

