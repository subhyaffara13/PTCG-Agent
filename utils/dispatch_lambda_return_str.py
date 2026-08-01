
def dispatch_lambda_return_str(f: NativeFunction) -> str:
    # [old codegen] Remove type annotation (e.g. 'Tensor' rather than 'Tensor &')
    # because the dispatch lambdas take mutable arguments *by value*, not
    # by reference. If you then return a reference to such an argument, you
    # will now have a pointer to a dangling stack entry. Not good.
    #
    # You want:
    #
    #   auto dispatch_selu_ = [](Tensor self) -> Tensor { ...; return at::selu_(self); };
    #                                            ^^^^^^
    #
    # *not*
    #
    #   auto dispatch_selu_ = [](Tensor self) -> Tensor& { ...; return at::selu_(self); };
    #                                            ^^^^^^^
    #
    # (NB: We can't make dispatch_selu_ take Tensor&, because the enclosing
    # codegen looks like dispatch_selu_(_r.tensor(0)), and you can't take a
    # mutable reference to temporary.  Maybe we could assign it to a
    # variable itself.)
    returns_without_annotation = tuple(
        Return(r.name, r.type, None) for r in f.func.returns
    )
    return_str = cpp.returns_type(returns_without_annotation, symint=True).cpp_type()
    if return_str not in SUPPORTED_RETURN_TYPES:
        raise RuntimeError(f"{f.func.name} returns unsupported type {return_str}")
    return return_str

