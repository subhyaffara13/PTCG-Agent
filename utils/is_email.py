
def is_email(instance: object) -> bool:
    if not isinstance(instance, str):
        return True
    return "@" in instance

