
def has_custom_eq_checks(t: Type) -> bool:
    return custom_special_method(t, "__eq__", check_all=False) or custom_special_method(
        t, "__ne__", check_all=False
    )

