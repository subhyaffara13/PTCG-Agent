
def stub_arguments(g: NativeFunctionsGroup) -> list[Binding]:
    # stubs drop all tensor arguments (they are implicit in the TensorIterator
    # argument and keep everything else)
    return [
        r
        for a in g.out.func.arguments.flat_non_out
        if not a.type.is_tensor_like()
        for r in structured.argument(a)
    ]

