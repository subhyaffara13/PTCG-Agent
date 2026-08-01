
def pep517_backend_reference(value: str) -> bool:
    """See PyPA's specification for defining build-backend references
    introduced in :pep:`517#source-trees`.

    This is similar to an entry-point reference (e.g., ``package.module:object``).
    """
    module, _, obj = value.partition(":")
    identifiers = (i.strip() for i in _chain(module.split("."), obj.split(".")))
    return all(python_identifier(i) for i in identifiers if i)

