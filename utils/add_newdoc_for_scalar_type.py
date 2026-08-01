
def add_newdoc_for_scalar_type(name: str, text_signature: str, doc: str) -> None:
    # note: `:field: value` is rST syntax which renders as field lists.
    cls = getattr(_numerictypes, name)
    module = cls.__module__

    lines_extra = [
        "",  # blank line after main doc
        f":Character code: ``{dtype(cls).char!r}``",
    ]

    if name != cls.__name__:
        lines_extra.append(f":Canonical name: `{module}.{name}`")

    lines_extra.extend(
        f"{_doc_alias_string} `{module}.{alias}`: {doc}."
        for alias_type, alias, doc in possible_aliases
        if alias_type is cls
    )

    docstring = _ARGUMENT_CLINIC_TEMPLATE.format(
        name=cls.__name__,  # must match the class name
        signature=text_signature,
        docstring="\n".join([doc.strip(), *lines_extra]),
    )
    add_newdoc('numpy._core.numerictypes', name, docstring)

