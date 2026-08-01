
def _raise_resolution_error(code: types.CodeType, scope: Any) -> Never:
    raise PackageError(
        f"Cannot resolve a fully qualified name for {code}. Lookup scope: {scope}"
    )

