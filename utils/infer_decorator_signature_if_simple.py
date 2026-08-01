
def infer_decorator_signature_if_simple(
    dec: Decorator, analyzer: SemanticAnalyzerInterface
) -> None:
    """Try to infer the type of the decorated function.

    This lets us resolve additional references to decorated functions
    during type checking. Otherwise, the type might not be available
    when we need it, since module top levels can't be deferred.

    This basically uses a simple special-purpose type inference
    engine just for decorators. Logic here should be kept in sync with
    visit_decorator() in mypy/checker.py.
    """
    if dec.var.is_property:
        # Decorators are expected to have a callable type (it's a little odd).
        # TODO: this may result in wrong type if @property is applied to decorated method.
        if dec.func.type is None:
            dec.var.type = CallableType(
                [AnyType(TypeOfAny.special_form)],
                [ARG_POS],
                [None],
                AnyType(TypeOfAny.special_form),
                analyzer.named_type("builtins.function"),
                name=dec.var.name,
            )
        elif isinstance(dec.func.type, CallableType):
            dec.var.type = dec.func.type
        return
    decorator_preserves_type = True
    for expr in dec.decorators:
        preserve_type = False
        if isinstance(expr, RefExpr) and isinstance(expr.node, FuncDef):
            if expr.fullname == "typing.no_type_check":
                return
            if expr.node.type and is_identity_signature(expr.node.type):
                preserve_type = True
        if not preserve_type:
            decorator_preserves_type = False
            break
    if decorator_preserves_type:
        # No non-identity decorators left. We can trivially infer the type
        # of the function here.
        sig = function_type(dec.func, analyzer.named_type("builtins.function"))
        dec.var.type = set_callable_name(sig, dec.func)
    if dec.decorators:
        return_type = calculate_return_type(dec.decorators[0])
        if return_type and isinstance(return_type, AnyType):
            # The outermost decorator will return Any so we know the type of the
            # decorated function.
            dec.var.type = AnyType(TypeOfAny.from_another_any, source_any=return_type)
        sig = find_fixed_callable_return(dec.decorators[0])
        if sig:
            # The outermost decorator always returns the same kind of function,
            # so we know that this is the type of the decorated function.
            orig_sig = function_type(dec.func, analyzer.named_type("builtins.function"))
            sig.name = orig_sig.items[0].name
            dec.var.type = sig
            if isinstance(sig, CallableType):
                sig.definition = dec

