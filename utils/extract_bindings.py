
def extract_bindings(f: NativeFunction) -> list[Binding]:
    return [
        r
        for a in f.func.schema_order_arguments()
        for r in cpp.argument(
            a,
            method=False,
            symint=True,
            cpp_no_default_args=set(),
            faithful=False,
            has_tensor_options=False,
        )
    ]

