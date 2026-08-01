
def verify_mypyfile(
    stub: nodes.MypyFile, runtime: MaybeMissing[types.ModuleType], object_path: list[str]
) -> Iterator[Error]:
    if isinstance(runtime, Missing):
        yield Error(object_path, "is not present at runtime", stub, runtime)
        return
    if not isinstance(runtime, types.ModuleType):
        # Can possibly happen:
        yield Error(object_path, "is not a module", stub, runtime)  # type: ignore[unreachable]
        return

    runtime_all_as_set: set[str] | None

    if hasattr(runtime, "__all__"):
        runtime_all_as_set = set(runtime.__all__)
        if "__all__" in stub.names:
            # Only verify the contents of the stub's __all__
            # if the stub actually defines __all__
            yield from _verify_exported_names(object_path, stub, runtime_all_as_set)
        else:
            yield Error(object_path + ["__all__"], "is not present in stub", MISSING, runtime)
    else:
        runtime_all_as_set = None

    # Check things in the stub
    to_check = {m for m, o in stub.names.items() if not o.module_hidden}

    def _belongs_to_runtime(r: types.ModuleType, attr: str) -> bool:
        """Heuristics to determine whether a name originates from another module."""
        obj = getattr(r, attr)
        if isinstance(obj, types.ModuleType):
            return False

        symbol_table = _module_symbol_table(r)
        if symbol_table is not None:
            try:
                symbol = symbol_table.lookup(attr)
            except KeyError:
                pass
            else:
                if symbol.is_imported():
                    # symtable says we got this from another module
                    return False
                # But we can't just return True here, because symtable doesn't know about symbols
                # that come from `from module import *`
                if symbol.is_assigned():
                    # symtable knows we assigned this symbol in the module
                    return True

        # The __module__ attribute is unreliable for anything except functions and classes,
        # but it's our best guess at this point
        try:
            obj_mod = obj.__module__
        except Exception:
            pass
        else:
            if isinstance(obj_mod, str):
                return bool(obj_mod == r.__name__)
        return True

    runtime_public_contents = (
        runtime_all_as_set
        if runtime_all_as_set is not None
        else {
            m
            for m in dir(runtime)
            if not is_probably_private(m)
            # Filter out objects that originate from other modules (best effort). Note that in the
            # absence of __all__, we don't have a way to detect explicit / intentional re-exports
            # at runtime
            and _belongs_to_runtime(runtime, m)
        }
    )
    # Check all things declared in module's __all__, falling back to our best guess
    to_check.update(runtime_public_contents)
    to_check.difference_update(IGNORED_MODULE_DUNDERS)

    for entry in sorted(to_check):
        stub_entry = stub.names[entry].node if entry in stub.names else MISSING
        if entry in stub.names:
            if xref := stub.names[entry].cross_ref:
                orig_module = xref.rsplit(".", 1)[0]
            elif isinstance(stub_entry, nodes.SymbolNode) and (name := stub_entry.fullname):
                orig_module = name.rsplit(".", 1)[0]
            else:
                orig_module = None

            if orig_module and orig_module != stub.fullname and orig_module in _all_stubs:
                # Skip re-exported names whose defining module will be checked separately.
                continue

        if isinstance(stub_entry, nodes.MypyFile):
            # Don't recursively check exported modules, since that leads to infinite recursion
            continue
        assert stub_entry is not None
        if (
            is_probably_private(entry)
            and not hasattr(runtime, entry)
            and not isinstance(stub_entry, Missing)
            and not _is_decoratable(stub_entry)
        ):
            # Skip private names that don't exist at runtime and which cannot
            # be marked with @type_check_only.
            continue
        try:
            runtime_entry = getattr(runtime, entry, MISSING)
        except Exception:
            # Catch all exceptions in case the runtime raises an unexpected exception
            # from __getattr__ or similar.
            continue
        yield from verify(stub_entry, runtime_entry, object_path + [entry])

