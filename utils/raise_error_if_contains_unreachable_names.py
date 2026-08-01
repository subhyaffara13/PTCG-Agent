
def raise_error_if_contains_unreachable_names(
    builder: IRBuilder, gen: GeneratorExpr | DictionaryComprehension
) -> bool:
    """Raise a runtime error and return True if generator contains unreachable names.

    False is returned if the generator can be safely transformed without crashing.
    (It may still be unreachable!)
    """
    if any(isinstance(s, NameExpr) and s.node is None for s in gen.indices):
        error = RaiseStandardError(
            RaiseStandardError.RUNTIME_ERROR,
            "mypyc internal error: should be unreachable",
            gen.line,
        )
        builder.add(error)
        return True

    return False

