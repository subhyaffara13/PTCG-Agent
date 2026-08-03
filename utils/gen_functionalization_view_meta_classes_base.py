from typing import Callable

def gen_functionalization_view_meta_classes_base(
    selector: SelectiveBuilder,
    g: NativeFunctionsViewGroup,
    run: Callable[[ViewMetaSpecialization], list[str]],
) -> list[str]:
    if not selector.include_all_operators:
        return []

    if g.composite:
        return []

    return ViewMetaSpecialization.map(g, run)

