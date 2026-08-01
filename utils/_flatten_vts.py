
def _flatten_vts(vts: Iterable[VariableTracker]) -> list[VariableTracker]:
    from collections import deque

    from .dicts import ConstDictVariable
    from .lists import ListVariable

    vts = deque(vts)
    output = []

    while vts:
        vt = vts.popleft()

        if not vt.is_realized() and vt.peek_type() in (dict, list, tuple):  # type: ignore[attr-defined]
            vt.realize()

        if vt.is_realized():
            if isinstance(vt, ListVariable):
                vts.extend(vt.items)
                continue
            elif isinstance(vt, ConstDictVariable):
                vts.extend(vt.items.values())
                continue

        output.append(vt)

    return output

