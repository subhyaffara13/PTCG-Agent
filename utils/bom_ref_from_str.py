from typing import Optional, Union

def bom_ref_from_str(bom_ref: BomRef, optional: bool = ...) -> BomRef:
    ...  # pragma: no cover


def bom_ref_from_str(bom_ref: Optional[str], optional: Literal[False] = False) -> BomRef:
    ...  # pragma: no cover


def bom_ref_from_str(bom_ref: Optional[str], optional: Literal[True] = ...) -> Optional[BomRef]:
    ...  # pragma: no cover


def bom_ref_from_str(bom_ref: Optional[Union[str, BomRef]], optional: bool = False) -> Optional[BomRef]:
    if isinstance(bom_ref, BomRef):
        return bom_ref
    if bom_ref:
        return BomRef(value=str(bom_ref))
    return None \
        if optional \
        else BomRef()

