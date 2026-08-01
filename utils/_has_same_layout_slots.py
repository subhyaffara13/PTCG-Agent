
def _has_same_layout_slots(
    slots: list[nodes.Const | None], assigned_value: nodes.Name
) -> bool:
    inferred = next(assigned_value.infer())
    if isinstance(inferred, nodes.ClassDef):
        other_slots = inferred.slots()
        if all(
            first_slot and second_slot and first_slot.value == second_slot.value
            for (first_slot, second_slot) in zip_longest(slots, other_slots)
        ):
            return True
    return False

