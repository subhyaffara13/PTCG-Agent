from typing import List, Optional

def buildPaletteLabels(
    labels: Iterable[_OptionalLocalizedString], nameTable: _n_a_m_e.table__n_a_m_e
) -> List[Optional[int]]:
    return [
        (
            nameTable.addMultilingualName(l, mac=False)
            if isinstance(l, dict)
            else (
                C_P_A_L_.table_C_P_A_L_.NO_NAME_ID
                if l is None
                else nameTable.addMultilingualName({"en": l}, mac=False)
            )
        )
        for l in labels
    ]

