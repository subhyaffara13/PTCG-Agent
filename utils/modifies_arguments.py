
def modifies_arguments(f: NativeFunction) -> bool:
    return any(
        a.annotation is not None and a.annotation.is_write
        for a in f.func.arguments.flat_all
    )


def modifies_arguments(f: NativeFunction) -> bool:
    return f.func.kind() in [SchemaKind.inplace, SchemaKind.out]

