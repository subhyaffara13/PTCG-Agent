
def specialize_parent_vtable(cls: ClassIR, parent: ClassIR) -> VTableEntries:
    """Generate the part of a vtable corresponding to a parent class or trait"""
    updated = []
    for entry in parent.vtable_entries:
        # Find the original method corresponding to this vtable entry.
        # (This may not be the method in the entry, if it was overridden.)
        orig_parent_method = entry.cls.get_method(entry.name, prefer_method=True)
        assert orig_parent_method
        method_cls = cls.get_method_and_class(entry.name, prefer_method=True)
        if method_cls:
            child_method, defining_cls = method_cls
            # TODO: emit a wrapper for __init__ that raises or something
            if (
                is_same_method_signature(orig_parent_method.sig, child_method.sig)
                or orig_parent_method.name == "__init__"
            ):
                entry = VTableMethod(entry.cls, entry.name, child_method, entry.shadow_method)
            else:
                entry = VTableMethod(
                    entry.cls,
                    entry.name,
                    defining_cls.glue_methods[(entry.cls, entry.name)],
                    entry.shadow_method,
                )
        updated.append(entry)
    return updated

