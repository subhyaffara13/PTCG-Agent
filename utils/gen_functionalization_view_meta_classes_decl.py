
def gen_functionalization_view_meta_classes_decl(
    selector: SelectiveBuilder, g: NativeFunctionsViewGroup
) -> list[str]:
    return gen_functionalization_view_meta_classes_base(
        selector, g, ViewMetaSpecialization.decl
    )

