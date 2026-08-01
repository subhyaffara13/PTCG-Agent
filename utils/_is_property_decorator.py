
def _is_property_decorator(decorator: nodes.Name) -> bool:
    for inferred in decorator.infer():
        if isinstance(inferred, nodes.ClassDef):
            if inferred.qname() in {"builtins.property", "functools.cached_property"}:
                return True
            for ancestor in inferred.ancestors():
                if ancestor.name == "property" and ancestor.root().name == "builtins":
                    return True
        elif isinstance(inferred, nodes.FunctionDef):
            # If decorator is function, check if it has exactly one return
            # and the return is itself a function decorated with property
            returns: list[nodes.Return] = list(
                inferred._get_return_nodes_skip_functions()
            )
            if len(returns) == 1 and isinstance(
                returns[0].value, (nodes.Name, nodes.Attribute)
            ):
                inferred = safe_infer(returns[0].value)
                if (
                    inferred
                    and isinstance(inferred, objects.Property)
                    and isinstance(inferred.function, nodes.FunctionDef)
                ):
                    return decorated_with_property(inferred.function)
    return False

