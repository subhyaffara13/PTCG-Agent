
def is_really_zero(class2: otTables.Class2Record) -> bool:
    v1 = getattr(class2, "Value1", None)
    v2 = getattr(class2, "Value2", None)
    return (v1 is None or v1.getEffectiveFormat() == 0) and (
        v2 is None or v2.getEffectiveFormat() == 0
    )

