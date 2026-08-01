
def _compile_fn(fn, in_structs):
  try:
    import torch  # pyrefly: ignore[missing-import]
  except ImportError:
    raise RuntimeError("Can't compile for PyTorch: import torch failed") from None

  traced = jax.jit(fn).trace(*in_structs)
  main_module = traced.lower().compiler_ir()
  with main_module.context:
    # jax.jit outlines its bodies which we undo for the interpreter.
    mgpu.dialect.register_inliner_extensions(main_module.context)
    inliner_pass = passmanager.PassManager.parse(
        "builtin.module(inline{default-pipeline=})"
    )
    inliner_pass.run(main_module.operation)
    mgpu_call, prepare_args, prepare_outputs, get_outputs = _find_mgpu_call_in_module(
        main_module
    )

  if not isinstance(in_structs, tuple):
    in_structs = (in_structs,)
  if isinstance(traced.out_info, tuple):
    out_structs = traced.out_info
    unwrap_output_tuple = False
  else:
    out_structs = (traced.out_info,)
    unwrap_output_tuple = True
  flat_arg_types, expected_arg_treedef = jax.tree.flatten(in_structs)
  _, out_treedef = jax.tree.flatten(out_structs)

  backend_config = mgpu_call.attributes["mhlo.backend_config"]
  module_asm = backend_config["module"].value_bytes
  launch, unload = mgpu_core._compile_as_torch_gpu_kernel(module_asm)

  def as_torch_dtype(dtype):
    # torch contains NumPy-compatible dtypes in its top namespace
    return getattr(torch, jnp.dtype(dtype).name)

  def apply(*user_args):
    flat_user_args, arg_treedef = jax.tree.flatten(user_args)
    if arg_treedef != expected_arg_treedef:
      raise ValueError(
          f"Invalid argument structure: expected {expected_arg_treedef}, got"
          f" {arg_treedef}, ({user_args=})"
      )
    for arg, expected_ty in zip(flat_user_args, flat_arg_types):
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

    # We run all the ops that are necessary to prepare the arguments
    device = torch.device("cuda")
    flat_args = prepare_args(*flat_user_args, device=device)
    flat_outs = prepare_outputs(*flat_args, device=device)
    # Construct a device pointer list like in the XLA calling convention
    buffers = (ctypes.c_void_p * (len(flat_args) + len(flat_outs)))()
    for i, arg in enumerate(itertools.chain(flat_args, flat_outs)):
      buffers[i] = arg.data_ptr()
    launch(buffers, device)
    user_outs = get_outputs(*flat_outs)
    out = jax.tree.unflatten(out_treedef, user_outs)
    return out[0] if unwrap_output_tuple else out

  # Unload the compiled code when the Python function is destroyed.
  # pyrefly: ignore[missing-attribute]
  apply.destructor = weakref.ref(apply, lambda _weak_ref: unload)

  return apply

