
def calculate_mro(info: TypeInfo, obj_type: Callable[[], Instance] | None = None) -> None:
    """Calculate and set mro (method resolution order).

    Raise MroError if cannot determine mro.
    """
    mro = linearize_hierarchy(info, obj_type)
    assert mro, f"Could not produce a MRO at all for {info}"
    info.mro = mro
    # The property of falling back to Any is inherited.
    info.fallback_to_any = any(baseinfo.fallback_to_any for baseinfo in info.mro)
    type_state.reset_all_subtype_caches_for(info)

