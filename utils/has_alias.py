
def has_alias(
    arguments: Sequence[Argument | SelfArgument | TensorOptionsArguments],
) -> bool:
    for arg in arguments:
        annotation = getattr(arg, "annotation", None)
        if not annotation:
            continue
        alias_set = getattr(annotation, "alias_set", ())
        if alias_set:
            return True
    return False

