
def _local_scalar_dense(data):
    # This is interesting!  Most lowerings return tensors, so you can just
    # return the buffer you allocated and it will get used (or not used, if
    # it's dead.)  But _local_scalar_dense (aka item) returns an int,
    # not a Tensor, so you would have a type mismatch if you return a buffer;
    # we are obligated to return a sympy expression instead.  However,
    # we need to actually codegen the .item() call somehow.  We do this
    # by registering a faux buffer for the DynamicScalar IR node, which is
    # solely responsible for generating this .item().  The buffer is
    # not used for anything (notice we discard it); at codegen time,
    # the "buffer" just gets assigned None.
    unbacked_bindings = resolve_unbacked_bindings(
        V.graph.sizevars.shape_env, V.graph.current_node.meta["unbacked_bindings"]
    )
    assert unbacked_bindings is not None
    assert len(unbacked_bindings) == 1, unbacked_bindings
    # NB: Have to be very careful here.  V.graph.current_node.meta["val"]
    # seemingly also contains a symbol which you want to do binding for,
    # but it actually isn't.  In particular, if we have later performed
    # a deferred runtime assert saying that u0 == s0, you will actually
    # see s0 from expr!  This is bad because we need to actually generate
    # the assert that says u0 == s0, so we need to know where to get u0
    # from (this call).  In particular, we must use unbacked_bindings, which
    # is guaranteed to have the original, unreplaced symbol in question.
    #
    # NB2: Another thing we have to be very careful about are symbol bindings
    # that require nontrivial refinement, e.g., when you have a binding site
    # x: Sym(u0 * 4) = y.item().  Here, the code generation must do a division
    # in order to appropriately bind u0.  This is communicated via the keypath
    # in unbacked_bindings, and we need to hold onto it in order to generate
    # code appropriately for this case.
    binding_sym, keypath = next(iter(unbacked_bindings.items()))
    buffer = ir.DynamicScalar(binding_sym, keypath, data)
    buffer.name = V.graph.register_buffer(buffer)
    V.graph.register_operation(buffer)
    # NB: the replaced expr is OK to use directly downstream, we want
    # simplifications in this case!
    val = V.graph.current_node.meta["val"]
    if isinstance(val, (torch.SymInt, torch.SymFloat, torch.SymBool)):
        return val.node.expr
    else:
        return sympy.sympify(val)


def _local_scalar_dense(func, *args, **kwargs):
    if not _maybe_get_mask(args[0]):
        raise ValueError(f"__torch_dispatch__, {func}: expected a mask tensor")
    return torch.ops.aten._local_scalar_dense(_get_data(args[0]))

