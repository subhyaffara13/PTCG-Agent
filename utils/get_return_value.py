
def get_return_value(f: NativeFunction) -> str:
    names = cpp.return_names(f)
    if len(f.func.returns) == 1:
        return names[0]
    if f.func.kind() == SchemaKind.out:
        return f"std::forward_as_tuple({', '.join(names)})"
    else:
        moved = ", ".join(f"std::move({name})" for name in names)
        return f"std::make_tuple({moved})"

