
def _make_custom_gradient_fn_tf(fun_jax,
                                *,
                                impl: NativeSerializationImpl,
                                with_gradient: bool,
                                args_specs, kwargs_specs,
                                args_tf: Sequence[TfVal],
                                outs_avals: Sequence[core.ShapedArray],
                                outs_tf: Sequence[TfVal]):
  """Prepares the TF function to be used with tf.custom_gradient.

  Args:
    impl: the serialization implementation details
    with_gradient: whether to include a tf.custom_gradient
    args_specs, kwargs_specs: the jax.ShapeDtypeArrays for the args and kwargs
    args_tf: the flattened TF arguments of the primal function
    outs_avals: the flattened output JAX abstract values of the primal function
    outs_tf: the flattened TF outputs of the primal function
  """
  def grad_fn_tf(*out_cts_flat_tf: TfVal,
                 variables=None):
    if variables:
      raise ValueError(
          "Unexpected variables used in forward pass. "
          "This should not happen for first-order differentiation. "
          f"{variables=}")

    # TODO: enable higher-order gradients
    with tf.name_scope("jax2tf_vjp"):
      def fix_out_ct(out_ct_tf, out_ct_aval: core.ShapedArray, out_tf: TfVal):
        # If the primal function has outputs of integer or bool types, and if we are
        # under a tf.function context, then TF will pass None in _out_cts_flat
        # in place of these values. We should change these to float0 or
        # else JAX gets unhappy. See issue #6975.
        if out_ct_tf is not None:
          return out_ct_tf
        assert core.primal_dtype_to_tangent_dtype(out_ct_aval.dtype) == dtypes.float0, f"{out_ct_tf=}"
        # Note that out_ct_aval.shape contains dimension variable from the
        # primal function scope. We use tf.zeros_like to make a 0 of the right shape.
        return tf.zeros_like(out_tf, dtype=_tf_np_dtype_for_float0)  # pyrefly: ignore [no-matching-overload]

      out_cts_fixed_flat_tf = tuple(map(fix_out_ct, out_cts_flat_tf, outs_avals, outs_tf))
      vjp_args_flat_tf = tuple(args_tf) + out_cts_fixed_flat_tf

      fun_vjp_jax, vjp_in_avals = impl.get_vjp_fun()

      vjp_polymorphic_shapes = tuple(
        # pyrefly: ignore[missing-attribute]
        str(a.shape)  # Note: may be _DimExpr, not just DimVar
        for a in vjp_in_avals)
      in_cts_flat = convert(
        fun_vjp_jax,
        with_gradient=with_gradient,
        polymorphic_shapes=vjp_polymorphic_shapes,
        **impl.convert_kwargs)(*vjp_args_flat_tf)

    # We do not need to fix the in_cts because the TF gradient machinery
    # will adjust the unconnected gradients and those for integer types.
    return in_cts_flat

  return grad_fn_tf

