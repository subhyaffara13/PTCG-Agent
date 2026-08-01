
def emit_view_functionalization_body(
    g: NativeFunctionsViewGroup, *, view_inplace: bool
) -> str:
    if view_inplace:
        # This op is both an inplace op AND a view op.
        # See Note [Functionalization Pass - Inplace View Ops] for details.
        # I currently have the view meta call into the out-of-place variant of the view, to avoid
        # having to define an extra ~20 inplace {view}_inverse_ functions.
        # Most view ops don't have NativeFunctionGroup's both, because we don't define out= variants for view ops.
        # I'm assuming that every inplace-view op has a corresponding out-of-place view op,
        # with the same name but the trailing underscore removed.
        # This is currently asserted at parse time in gen.py (see error_check_native_functions).
        if g.view_inplace is None:
            raise AssertionError(
                "Expected view_inplace to be non-None for inplace view"
            )
        f = g.view_inplace
    else:
        f = g.view

    if g.view_copy is None:
        raise AssertionError("Expected view_copy to be non-None")
    with native_function_manager(f):
        call_sig = DispatcherSignature.from_schema(g.view_copy.func)

        spec = ViewMetaSpecialization(g, f=f)

        # the "view_copy" op name that the functionalization kernels need to call
        api_name = g.view_copy.func.name.unambiguous_name()
        # Sometimes the functionalization pass needs to no-op (e.g. if it was passed non-functional tensors)
        # "no-op"ing in this context is just redispatching to the original op.
        noop_api_name = f.func.name.unambiguous_name()

        dispatcher_sig = DispatcherSignature.from_schema(f.func)
        assert_view_op_properties(f.func)
        view_tensor_name = dispatcher_sig.arguments()[0].name

        return_type = dispatcher_sig.returns_type().remove_const_ref().cpp_type()

        unwrap_tensor_args_str, unwrapped_args_ctx = unwrap_tensor_args(
            dispatcher_sig, is_view_op=True
        )
        view_redispatch_args = [
            e.expr
            for e in translate(unwrapped_args_ctx, call_sig.arguments(), method=False)
        ]

        # The meta API call should use the same arguments, but convert all tensors to meta tensors first.
        meta_conversion_str, meta_call_ctx = convert_to_meta_tensors(dispatcher_sig)
        meta_call_args = [
            e.expr for e in translate(meta_call_ctx, call_sig.arguments(), method=False)
        ]

        (
            symbolic_inputs_varname,
            symbolic_inputs_check,
        ) = emit_has_symbolic_inputs(call_sig)

        if "inplace_view" in f.tags:
            # See Note [Functionalization Pass - Inplace View Ops] for more details
            return f"""
    {dispatcher_sig.defn(name=wrapper_name(f.func), is_redispatching_fn=True)} {{
      if (!at::functionalization::impl::isFunctionalTensor({view_tensor_name})) {{
        // functionalization is re-entrant, but will no-op if it wasn't passed a FunctionalTensorWrapper.
        {unwrap_tensor_args_str}
        at::AutoDispatchSkipFunctionalize guard;
        return at::_ops::{noop_api_name}::call({", ".join(view_redispatch_args)});
      }}
      auto reapply_views = at::functionalization::impl::getFunctionalizationReapplyViewsTLS();
      auto inverse_return_mode = (
          reapply_views ? at::functionalization::InverseReturnMode::ViewOrScatterInverse
            : at::functionalization::InverseReturnMode::NeverView
      );
      {symbolic_inputs_check}
      auto view_meta = {spec.new()};
      auto compute_reference_meta =
        {view_tensor_name}.key_set().has_backend(c10::BackendComponent::XLABit) ||
        {view_tensor_name}.key_set().has_backend(c10::BackendComponent::LazyBit);
      {return_type} reference_tensor_output;
      if (compute_reference_meta && !disable_meta_reference()) {{
        {meta_conversion_str}
        at::AutoDispatchSkipFunctionalize func_guard;
        c10::impl::ExcludeDispatchKeyGuard guard(exclude_keys_for_meta_dispatch);
        reference_tensor_output = at::_ops::{noop_api_name}::call({", ".join(meta_call_args)});
      }}
      // This function adds the above view meta to the current tensor and replays them off the base,
      // mutating the size/stride info of the current FunctionalTensorWrapper.
      // Because of this, we need to make sure to run the reference shape function above,
      // BEFORE doing this (otherwise we'll end up running the reference function using the wrong sizes/strides)
      at::functionalization::impl::mutate_view_meta({view_tensor_name}, view_meta);
      // See  Note [Propagating strides in the functionalization pass]
      // XLA/LTC don't implement the logic to propagate strides correctly, so we need to rely
      // on a reference implementation here (instead of relying on the output from the forward lambda
      // having the correct stride info)
      if (compute_reference_meta && !disable_meta_reference()) {{
        at::functionalization::impl::set_sizes_strides_offset({view_tensor_name}, reference_tensor_output);
      }}
      return {view_tensor_name};
    }}
"""

        else:
            return f"""
    {dispatcher_sig.defn(name=wrapper_name(f.func), is_redispatching_fn=True)} {{
      {unwrap_tensor_args_str}
      if (!at::functionalization::impl::isFunctionalTensor({view_tensor_name})) {{
        // functionalization is re-entrant, but will no-op if it wasn't passed a FunctionalTensorWrapper.
        at::AutoDispatchSkipFunctionalize guard;
        return at::_ops::{noop_api_name}::call({", ".join(view_redispatch_args)});
      }}
      auto reapply_views = at::functionalization::impl::getFunctionalizationReapplyViewsTLS();
      auto inverse_return_mode = (
          reapply_views ? at::functionalization::InverseReturnMode::ViewOrScatterInverse
            : at::functionalization::InverseReturnMode::NeverView
      );
      auto compute_reference_meta =
        {view_tensor_name}.key_set().has_backend(c10::BackendComponent::XLABit) ||
        {view_tensor_name}.key_set().has_backend(c10::BackendComponent::LazyBit);
      {return_type} reference_tensor_output;
      if (compute_reference_meta && !disable_meta_reference()) {{
        {meta_conversion_str}
        at::AutoDispatchSkipFunctionalize func_guard;
        c10::impl::ExcludeDispatchKeyGuard guard(exclude_keys_for_meta_dispatch);
        reference_tensor_output = at::_ops::{noop_api_name}::call({", ".join(meta_call_args)});
      }}
      {return_type} tmp_output;
      {{
        at::AutoDispatchSkipFunctionalize guard;
        if (reapply_views) {{
          tmp_output = at::_ops::{noop_api_name}::call({", ".join(view_redispatch_args)});
        }} else {{
          tmp_output = at::_ops::{api_name}::call({", ".join(view_redispatch_args)});
        }}
      }}
      {symbolic_inputs_check}
      auto view_meta = {spec.new()};
      auto out = at::functionalization::impl::create_functional_tensor_with_view_meta(tmp_output, {view_tensor_name}, view_meta);
      // See  Note [Propagating strides in the functionalization pass]
      if (compute_reference_meta && !disable_meta_reference()) {{
        at::functionalization::impl::set_sizes_strides_offset(out, reference_tensor_output);
      }}
      return out;
    }}
"""

