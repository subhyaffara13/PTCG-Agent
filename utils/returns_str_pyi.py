
def returns_str_pyi(signature: PythonSignature) -> str:
    field_names = structseq_fieldnames(signature.returns.returns)
    if field_names:
        return f"torch.return_types.{signature.name}"

    python_returns = [return_type_str_pyi(r.type) for r in signature.returns.returns]
    if len(python_returns) > 1:
        return "tuple[" + ", ".join(python_returns) + "]"
    if len(python_returns) == 1:
        return python_returns[0]
    return "None"

