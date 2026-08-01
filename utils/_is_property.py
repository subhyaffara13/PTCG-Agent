
def _is_property(
    meth: nodes.FunctionDef | UnboundMethod, context: InferenceContext | None = None
) -> bool:
    decoratornames = meth.decoratornames(context=context)
    if PROPERTIES.intersection(decoratornames):
        return True
    stripped = {
        name.split(".")[-1]
        for name in decoratornames
        if not isinstance(name, UninferableBase)
    }
    if any(name in stripped for name in POSSIBLE_PROPERTIES):
        return True

    if not meth.decorators:
        return False
    # Lookup for subclasses of *property*
    for decorator in meth.decorators.nodes or ():
        inferred = safe_infer(decorator, context=context)
        if inferred is None or isinstance(inferred, UninferableBase):
            continue
        if isinstance(inferred, nodes.ClassDef):
            # Check for a class which inherits from a standard property type
            if any(inferred.is_subtype_of(pclass) for pclass in PROPERTIES):
                return True
            for base_class in inferred.bases:
                # Check for a class which inherits from functools.cached_property
                # and includes a subscripted type annotation
                if isinstance(base_class, nodes.Subscript):
                    value = safe_infer(base_class.value, context=context)
                    if not isinstance(value, nodes.ClassDef):
                        continue
                    if value.name != "cached_property":
                        continue
                    module, _ = value.lookup(value.name)
                    if isinstance(module, nodes.Module) and module.name == "functools":
                        return True
                    continue

    return False

