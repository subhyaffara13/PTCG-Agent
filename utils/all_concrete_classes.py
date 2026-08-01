
def all_concrete_classes(class_ir: ClassIR) -> list[ClassIR] | None:
    """Return all concrete classes among the class itself and its subclasses."""
    concrete = class_ir.concrete_subclasses()
    if concrete is None:
        return None
    if not (class_ir.is_abstract or class_ir.is_trait):
        concrete.append(class_ir)
    return concrete

