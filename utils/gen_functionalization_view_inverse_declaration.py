
def gen_functionalization_view_inverse_declaration(
    selector: SelectiveBuilder, g: NativeFunctionsViewGroup
) -> str | None:
    # For every (non-composite) view op, we need a corresponding "inverse view" function.
    # This generates the declarations so we get a good compiler error when someone adds a new view.
    @with_native_function
    def emit_decl_helper(g: NativeFunctionsViewGroup) -> str | None:
        if g.view.has_composite_implicit_autograd_kernel:
            return None
        view_inverse_sig = ViewInverseSignature(g)
        return view_inverse_sig.decl()

    return emit_decl_helper(g)

