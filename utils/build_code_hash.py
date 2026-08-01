
def build_code_hash(
    roots: list[str] | None, prefix: str, hasher: hashlib._Hash
) -> None:
    for lib in sorted(pkgutil.iter_modules(roots, prefix), key=lambda x: x.name):
        spec = lib.module_finder.find_spec(lib.name, None)
        assert spec is not None
        module = spec.origin
        assert module is not None
        with open(module, "rb") as f:
            hasher.update(spec.name.encode("utf-8"))
            hasher.update(f.read())
        if lib.ispkg:
            # need to also hash submodules
            build_code_hash(spec.submodule_search_locations, f"{spec.name}.", hasher)

