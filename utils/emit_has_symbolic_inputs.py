
def emit_has_symbolic_inputs(sig: DispatcherSignature) -> tuple[str, str]:
    name = "has_symbolic_inputs"
    statements = [
        f"{name} = {name} | ({emit_expr_has_symbolic_values(binding.name, binding.nctype.type)});"
        for binding in sig.arguments()
        if (
            isinstance(binding.argument, Argument)
            and binding.argument.type.is_symint_like()
        )
    ]
    body = "\n      ".join(statements)
    return (
        name,
        f"""
      bool {name} = false;
      {body}""",
    )

