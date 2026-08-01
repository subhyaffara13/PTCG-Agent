
def is_special_form_any(t: AnyType) -> bool:
    return get_original_any(t).type_of_any == TypeOfAny.special_form

