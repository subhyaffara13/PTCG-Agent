
def python_entrypoint_reference(value: str) -> bool:
    """Reference to a Python object using in the format::

        importable.module:object.attr

    See ``Data model >object reference`` in the :ref:`PyPA's entry-points specification
    <pypa:entry-points>`.
    """
    module, _, rest = value.partition(":")
    if "[" in rest:
        obj, _, extras_ = rest.partition("[")
        if extras_.strip()[-1] != "]":
            return False
        extras = (x.strip() for x in extras_.strip(string.whitespace + "[]").split(","))
        if not all(pep508_identifier(e) for e in extras):
            return False
        _logger.warning(f"`{value}` - using extras for entry points is not recommended")
    else:
        obj = rest

    module_parts = module.split(".")
    identifiers = _chain(module_parts, obj.split(".")) if rest else iter(module_parts)
    return all(python_identifier(i.strip()) for i in identifiers)

