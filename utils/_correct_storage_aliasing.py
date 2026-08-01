
def _correct_storage_aliasing(func, schema_info, args, outs) -> None:
    """
    Given: an OpOverload, a SchemaInfo (cached information from torchgen about schema),
    and the inputs/outputs to the OpOverload,
    this function checks to see if func is a view operator
    (by checking if any of the outputs in the op's schema
     are immutable aliases of inputs).
    If so, this function manually aliases the storage of the output tensor
    with its corresponding input tensor alias.
    It does this by unsafely overwriting the storage field of the output tensor
    to be the same storage as the input.
    """
    if not isinstance(func, torch._ops.OpOverload):
        raise AssertionError(f"func must be an OpOverload, got {type(args)}")
    if not isinstance(args, tuple):
        raise AssertionError(f"args must be a tuple, got {type(args)}")
    if not isinstance(outs, (list, tuple)):
        raise AssertionError(f"outs must be a list or tuple, got {type(args)}")

    def alias_non_inplace_storage(arg, ret) -> None:
        # This is hopefully a reasonable assert:
        # subclasses that rely on this API for output aliasing
        # should always return wrapper tensor subclasses for us to manually alias.
        # in theory if a subclass that needs this API wants to sometimes return
        # plain tensors, we could remove the assert and just not perform the aliasing,
        # but it seems safer to learn more about this case first.
        #
        # Performance note: This is all just to assert that the argument and result
        # types match, checking that is cheaper than is_traceable_wrapper_subclass_type,
        # and multiple returns are relatively unlikely, so just check up front!
        arg_type = type(arg)
        ret_type = type(ret)
        if arg_type is not ret_type and (
            is_traceable_wrapper_subclass_type(arg_type)
            or is_traceable_wrapper_subclass_type(ret_type)
        ):
            ret_list = ret if isinstance(ret, list) else [ret]
            for r in ret_list:
                if type(arg) is not type(r):
                    raise AssertionError(
                        f"Called {str(func)} with input of type {type(arg)}\n"
                        f"and output of type {type(ret)}. But expected types to match."
                    )
        # Need to call a non-dispatcher helper, because we explicitly do **not**
        # want our subclass to intercept the set_() call.
        # instead, our subclass should directly have its storage swapped out.
        # we **explicitly** don't want to reset the sizes on ret, if the storage implies a size change.
        # Why?
        # The purpose of this API is *not* to change the size/strides of our output- we assume it's already correct.
        # We just want to "fix up" the storage aliasing, without modifying or output's metadata.
        # Example: out = inp.expand(inp.shape[0], inp.shape[0])
        #     This requires swapping the storage of out to be the same as inp,
        #     but we do *not* want it to change the sizes/strides that were compute for out.

        if isinstance(ret, list):
            for r in ret:
                torch._functionalize_unsafe_set(r, arg)
        else:
            if not isinstance(ret, torch.Tensor):
                raise AssertionError(f"expected torch.Tensor, got {type(ret)}")
            torch._functionalize_unsafe_set(ret, arg)

    for arg_idx, return_idx in schema_info.read_only_alias_match_indexes:
        alias_non_inplace_storage(args[arg_idx], outs[return_idx])

