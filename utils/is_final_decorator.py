
def is_final_decorator(d: Expression) -> bool:
    return refers_to_fullname(d, FINAL_DECORATOR_NAMES)

