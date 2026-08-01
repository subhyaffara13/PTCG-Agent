
def tie_return_values(f: NativeFunction) -> str:
    if len(f.func.returns) == 1:
        return f"auto {f.func.returns[0].name or 'result'}"
    names = cpp.return_names(f)
    return f"auto [{', '.join(names)}]"

