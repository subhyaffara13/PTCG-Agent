
def record_nn_module_stack(
    module_key: str, source: Source, tx: "InstructionTranslator", mod: torch.nn.Module
) -> Any:
    fully_qualified_name = source.name
    # Remove redundant namings
    fully_qualified_name = re.sub(
        r"\._(?:modules|parameters|buffers)\[(['\"])([^'\"\]]+)\1\]",
        r".\2",
        fully_qualified_name,
    )
    num_calls = tx.num_calls.get(fully_qualified_name, 0)
    module_key = f"{module_key}@{num_calls}" if num_calls > 0 else module_key
    try:
        tx.nn_module_stack[module_key] = (fully_qualified_name, mod.__class__)
        tx.num_calls[fully_qualified_name] = num_calls + 1
        yield
    finally:
        del tx.nn_module_stack[module_key]

