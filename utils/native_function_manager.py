
def native_function_manager(
    g: NativeFunctionsGroup | NativeFunctionsViewGroup | NativeFunction,
) -> Iterator[None]:
    if isinstance(g, NativeFunctionsGroup):
        # By default, we associate all errors with structured native functions
        # with the out variant.  In some cases, it might be better to have
        # a more specific place to hang things; if so, use
        # native_function_manager again on the inside
        f = g.out
    elif isinstance(g, NativeFunctionsViewGroup):
        # We associate errors with the view operator
        f = g.view
    else:
        f = g
    with context(lambda: f"in native_functions.yaml line {f.loc}:\n  {f.func}"):
        with local.parametrize(
            use_const_ref_for_mutable_tensors=f.use_const_ref_for_mutable_tensors,
            use_ilistref_for_tensor_lists=f.part_of_structured_group,
        ):
            yield

