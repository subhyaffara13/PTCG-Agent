
def _get_unpacking_extra_info(node: nodes.Assign, inferred: InferenceResult) -> str:
    """Return extra information to add to the message for unpacking-non-sequence
    and unbalanced-tuple/dict-unpacking errors.
    """
    more = ""
    if isinstance(inferred, DICT_TYPES):
        match node:
            case nodes.Assign():
                more = node.value.as_string()
            case nodes.For():
                more = node.iter.as_string()
        return more

    inferred_module = inferred.root().name
    if node.root().name == inferred_module:
        if node.lineno == inferred.lineno:
            more = f"'{inferred.as_string()}'"
        elif inferred.lineno:
            more = f"defined at line {inferred.lineno}"
    elif inferred.lineno:
        more = f"defined at line {inferred.lineno} of {inferred_module}"
    return more

