
def detect_undefined_bitmap(cl: ClassIR, seen: set[ClassIR]) -> None:
    if cl.is_trait:
        return

    if cl in seen:
        return
    seen.add(cl)
    for base in cl.base_mro[1:]:
        detect_undefined_bitmap(base, seen)

    # Build fresh and assign once. This function is called per SCC and `seen`
    # only dedupes within a single call, so appending in place to a shared base
    # would accumulate duplicates across SCCs and produce non-deterministic
    # struct layouts under separate=True.
    new_attrs: list[str] = []
    if len(cl.base_mro) > 1:
        new_attrs.extend(cl.base_mro[1].bitmap_attrs)
    for n, t in cl.attributes.items():
        if t.error_overlap and not cl.is_always_defined(n):
            new_attrs.append(n)

    for base in cl.mro[1:]:
        if base.is_trait:
            for n, t in base.attributes.items():
                if t.error_overlap and not cl.is_always_defined(n) and n not in new_attrs:
                    new_attrs.append(n)
    cl.bitmap_attrs = new_attrs

