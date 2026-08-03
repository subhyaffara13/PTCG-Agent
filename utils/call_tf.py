from typing import Callable

def call_tf(
    callable_tf: Callable,
    has_side_effects=True,
    ordered=False,
    output_shape_dtype=UnspecifiedOutputShapeDtype(),
    call_tf_graph=False,
) -> Callable:
  """Calls a TensorFlow function from JAX, with support for reverse autodiff.

  The ``callable_tf`` will be called with TensorFlow-compatible arguments (
  numpy.ndarray, ``tf.Tensor`` or ``tf.Variable``) or pytrees thereof. The
  function must return the same type of results.

  If ``call_tf`` appears in a JAX staging context (:func:`jax.jit`,
  or :func:`jax.pmap`, or a control-flow primitive) then
  ``callable_tf`` will be compiled with ``tf.function(callable_tf,
  jit_compile=True)``
  and the resulting XLA computation will be embedded in JAX's XLA computation.

  If ``call_tf`` appears outside a JAX staging context, it will be called inline
  using TensorFlow eager mode.

  The ``call_tf`` supports JAX's reverse-mode autodiff, in which case the
  ``callable_tf`` will be differentiated using ``tf.GradientTape``. This means
  that the gradient will be TensorFlow-accurate, e.g., will respect the
  custom gradients that may be defined for the code in ``callable_tf``.

  For an example and more details see the
  `README
  <https://github.com/jax-ml/jax/blob/main/jax/experimental/jax2tf/README.md#calling-tensorflow-functions-from-jax>`_.

  Args:
    callable_tf: a TensorFlow Callable that can take a pytree of TensorFlow
      arguments.
    has_side_effects: if True then it ensures that instances of this primitive
      are not removed or replicated by JAX optimizations such as dead-code
      elimination.
    ordered: If true, calls are modeled as having ordered effects.
    output_shape_dtype: An optional declaration of the expected shape and dtype
      of the result of the called TensorFlow function. If given it will be used
      during JAX tracing to form the abstract values of the results of the
      `call_tf`. If not given then we form a `tf.Graph` for the called
      TensorFlow function and we use the TensorFlow-inferred shapes and types.
      Must be a pytree matching the structure of the nested structure returned
      from the TensorFlow function, containing objects with `.shape` and
      `.dtype` attributes, e.g., `jax.ShapeDtypeStruct` or `jax.Array`.
    call_tf_graph: EXPERIMENTAL, DO NOT USE. We may change the name in the
      future.

  Returns: a JAX callable that can be invoked with JAX pytree arguments, in
    op-by-op mode or in a staged context. This callable can be used with JAX's
    reverse-mode autodiff (:func:`jax.grad`).
  """
  @jax.custom_vjp
  def make_call(*args_jax):
    """We wrap it all in `make_call` so that we can attach custom VJP."""

    args_flat_jax, args_treedef = tree_util.tree_flatten(args_jax)
    # Canonicalize the arguments; e.g., makes them x32 if JAX is in 32-bit mode
    def canonical_arg(v):
      v = v if getattr(v, "dtype", None) else np.asarray(v)
      dtype = dtypes.canonicalize_dtype(v.dtype)
      if dtype != v.dtype:
        v = v.astype(dtype)
      return v

    args_flat_jax = tuple(map(canonical_arg, args_flat_jax))
    def make_tensorspec(a_jax):
      a_tf_dtype = jax2tf_internal._to_tf_dtype(a_jax.dtype)
      a_tf_shape = [d if core.is_constant_dim(d) else None for d in getattr(a_jax, "shape", ())]
      return tf.TensorSpec(a_tf_shape, a_tf_dtype)
    args_flat_sig_tf = tuple(map(make_tensorspec, args_flat_jax))

    if not isinstance(output_shape_dtype, UnspecifiedOutputShapeDtype):
      output_shape_dtype_flat, output_shape_dtype_tree = tree_util.tree_flatten(output_shape_dtype)
      output_avals = tuple(core.ShapedArray(st.shape, st.dtype) for st in output_shape_dtype_flat)
    else:
      output_avals, output_shape_dtype_tree = None, None

    res_treedef = None  # We'll store here the result treedef
    res_tf_flat = None  # For error reporting
    # The function below will be called at least once, either in eager
    # mode during jax2tf_call_tf or in graph mode during _get_concrete_function_tf()
    def callable_flat_tf(*args_tf_flat: TfVal) -> Sequence[TfVal]:
      args_tf = args_treedef.unflatten(args_tf_flat)
      res_tf = callable_tf(*args_tf)

      # b/279454591: When `callable_tf` is a tf function with zero outputs, it
      # returns a `StatefulPartitionedCall` (if the function is stateful) or
      # `PartitionedCall` (if the function is stateless) op instead of
      # tf.Tensors. We work around this issue by replacing the output `res_tf`
      # with an empty list.

      if isinstance(res_tf, tf.Operation):
        assert (
            res_tf.type == "StatefulPartitionedCall"
            or res_tf.type == "PartitionedCall"
        )
        t_out = res_tf.get_attr("Tout")
        # t_out should be an empty list.
        assert not t_out, (
            "The TF function returned an unexpected result, please check its"
            f" function body. res_tf = {res_tf}"
        )
        res_tf = t_out

      nonlocal res_treedef, res_tf_flat
      res_tf_flat, res_treedef_now = tree_util.tree_flatten(res_tf)
      assert res_treedef is None or res_treedef == res_treedef_now, (
          f"Subsequent calls had different results. Previous {res_treedef} and now {res_treedef_now}")
      res_treedef = res_treedef_now
      if output_avals is not None:
        if res_treedef != output_shape_dtype_tree:
          raise ValueError(
              "The pytree of the TensorFlow function results does not match the "
              "pytree of the declared output_shape_dtype:\n"
              f"results pytree: {res_treedef}\noutput_shape_dtype tree: {output_shape_dtype_tree}")
        assert len(output_avals) == len(res_tf_flat)

      checked_res_tf_flat = [
          check_tf_result(i, r_tf, r_aval)
          for i, (r_tf, r_aval) in enumerate(
              zip(res_tf_flat,
                  (output_avals
                   if output_avals is not None
                   else (None,) * len(res_tf_flat))))]
      return checked_res_tf_flat

    # Prepare a tf.function ahead of time, to cache the concrete functions. This
    # won't be used in op-by-op execution mode.
    function_flat_tf = tf.function(
        callable_flat_tf, autograph=False, jit_compile=not call_tf_graph)

    res_jax_flat = call_tf_p.bind(
        *args_flat_jax,
        # Carry the actual function such that op-by-op call can call in TF eager mode.
        callable_flat_tf=callable_flat_tf,
        function_flat_tf=function_flat_tf,
        args_flat_sig_tf=args_flat_sig_tf,
        output_avals=output_avals,
        has_side_effects=has_side_effects,
        ordered=ordered,
        call_tf_graph=call_tf_graph,
    )

    # We must have called callable_flat_tf by nοw
    assert res_treedef is not None
    return res_treedef.unflatten(res_jax_flat)

  # Define the fwd and bwd custom_vjp functions
  def make_call_vjp_fwd(*args_jax):
    # Return the primal arguments as the residual
    return make_call(*args_jax), args_jax

  def make_call_vjp_bwd(residual_jax, ct_res_jax):
    args_jax = residual_jax  # residual is the primal argument

    def tf_vjp_fun(args_tf, ct_res_tf):
      """Invoke TF gradient."""

      # TF does not like us to watch non-float vars or Nones.
      def replace_non_float_or_none(arg_tf):
        if arg_tf is not None and (
            arg_tf.dtype.is_floating or arg_tf.dtype.is_complex
        ):
          return arg_tf
        else:
          # When watched, this will be ignored. When used in results it will
          # result in a floating 0. gradient, which JAX will ignore (and
          # replace it with a float0)
          return tf.zeros((), dtype=tf.float32)

      watched_args_tf = tf.nest.map_structure(
          replace_non_float_or_none, args_tf
      )
      with tf.GradientTape(persistent=True) as tape:
        tape.watch(watched_args_tf)
        res = callable_tf(*args_tf)

      tf.nest.assert_same_structure(res, ct_res_tf)
      dres_darg = tape.gradient(
          tf.nest.map_structure(replace_non_float_or_none, res),
          sources=watched_args_tf,
          output_gradients=ct_res_tf,
          unconnected_gradients=tf.UnconnectedGradients.ZERO,
      )

      dres_darg = tree_util.tree_map(
          lambda x: x if x is None else tf.convert_to_tensor(x),
          dres_darg,
      )

      # callable_tf may mutate (the structure of) args_tf, thus we check against
      # watched_args_tf which should be structurally the same as the original
      # args_tf.
      tf.nest.assert_same_structure(dres_darg, watched_args_tf)
      return dres_darg

    # Use call_tf to call the VJP function
    ct_args_jax = call_tf(tf_vjp_fun)(args_jax, ct_res_jax)
    # We must make the float0s that JAX expects
    def fix_float0(arg_jax, ct_arg_jax):
      if arg_jax is None:
        return None
      arg_dtype = dtypes.result_type(arg_jax)  # May be scalar
      ct_arg_dtype = core.primal_dtype_to_tangent_dtype(arg_dtype)
      if ct_arg_dtype != ct_arg_jax.dtype:
        return ad_util.zeros_like_aval(core.ShapedArray(np.shape(arg_jax),
                                                        ct_arg_dtype))
      return ct_arg_jax

    ct_args_jax_fixed = tree_util.tree_map(fix_float0, args_jax, ct_args_jax,
                                           is_leaf=lambda x: x is None)
    return ct_args_jax_fixed

  make_call.defvjp(make_call_vjp_fwd, make_call_vjp_bwd)
  return util.wraps(callable_tf)(make_call)

