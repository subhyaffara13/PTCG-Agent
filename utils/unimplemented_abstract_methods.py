
def unimplemented_abstract_methods(
    node: nodes.ClassDef, is_abstract_cb: nodes.FunctionDef | None = None
) -> dict[str, nodes.FunctionDef]:
    """Get the unimplemented abstract methods for the given *node*.

    A method can be considered abstract if the callback *is_abstract_cb*
    returns a ``True`` value. The check defaults to verifying that
    a method is decorated with abstract methods.
    It will return a dictionary of abstract method
    names and their inferred objects.
    """
    if is_abstract_cb is None:
        is_abstract_cb = partial(decorated_with, qnames=ABC_METHODS)
    visited: dict[str, nodes.FunctionDef] = {}
    try:
        mro = reversed(node.mro())
    except astroid.ResolveError:
        # Probably inconsistent hierarchy, don't try to figure this out here.
        return {}
    for ancestor in mro:
        for obj in ancestor.values():
            inferred = obj
            if isinstance(obj, nodes.AssignName):
                inferred = safe_infer(obj)
                if not inferred:
                    # Might be an abstract function,
                    # but since we don't have enough information
                    # in order to take this decision, we're taking
                    # the *safe* decision instead.
                    if obj.name in visited:
                        del visited[obj.name]
                    continue
                if not isinstance(inferred, nodes.FunctionDef):
                    if obj.name in visited:
                        del visited[obj.name]
            if isinstance(inferred, nodes.FunctionDef):
                # It's critical to use the original name,
                # since after inferring, an object can be something
                # else than expected, as in the case of the
                # following assignment.
                #
                # class A:
                #     def keys(self): pass
                #     __iter__ = keys
                abstract = is_abstract_cb(inferred)
                if abstract:
                    visited[obj.name] = inferred
                elif not abstract and obj.name in visited:
                    del visited[obj.name]
    return visited

