
def _get_namedtuple_fields(node: nodes.Call) -> str:
    """Get and return fields of a NamedTuple in code-as-a-string.

    Because the fields are represented in their code form we can
    extract a node from them later on.
    """
    names = []
    container = None
    try:
        container = next(node.args[1].infer())
    except (InferenceError, StopIteration) as exc:
        raise UseInferenceDefault from exc
    # We pass on IndexError as we'll try to infer 'field_names' from the keywords
    except IndexError:
        pass
    if not container:
        for keyword_node in node.keywords:
            if keyword_node.arg == "field_names":
                try:
                    container = next(keyword_node.value.infer())
                except (InferenceError, StopIteration) as exc:
                    raise UseInferenceDefault from exc
                break
    if not isinstance(container, nodes.BaseContainer):
        raise UseInferenceDefault
    for elt in container.elts:
        if isinstance(elt, nodes.Const):
            names.append(elt.as_string())
            continue
        if not isinstance(elt, (nodes.List, nodes.Tuple)):
            raise UseInferenceDefault
        if len(elt.elts) != 2:
            raise UseInferenceDefault
        names.append(elt.elts[0].as_string())

    if names:
        field_names = f"({','.join(names)},)"
    else:
        field_names = ""
    return field_names

